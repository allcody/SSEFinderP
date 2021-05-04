from django.shortcuts import render, redirect
from django.http import HttpResponse
from covid.models import *
from datetime import datetime, date, timedelta
from django.forms import modelformset_factory, TextInput, CheckboxSelectMultiple
from django.contrib import messages
from django.views.generic import TemplateView 
# Create your views here.

def test(request):
    return HttpResponse("Hello world")

def CaseFormView(request):
    eventFormSet = modelformset_factory(Event, form = newEventForm, extra=1)

    if request.method == 'POST':
        form = CaseForm(request.POST)
        formset = eventFormSet(request.POST, request.FILES)

        '''
            Check the valid form first, then check the input date.
        '''
        if form.is_valid() and formset.is_valid():
            birth_date = form.cleaned_data['birth']
            onset_date = form.cleaned_data['onset_date']
            confirm_date = form.cleaned_data['confirm_date']
            deltaBO = onset_date - birth_date
            deltaCO = confirm_date - onset_date

            if (deltaBO > timedelta(days=0) and deltaCO > timedelta(days=0))  :
                for attended_event in form.cleaned_data['events']:
                    end_date = attended_event.date + timedelta(days=14)
                    
                    if onset_date > end_date or attended_event.date >confirm_date:
                        messages.error(request, "case date out of range")
                        return render(request, 'case_form.html', {'form': form, 'formset': formset})


                for new_event_form in formset:
                    if len(new_event_form.cleaned_data) == 0:
                        break
                    event_date = new_event_form.cleaned_data['date']
                    # start_date = event_date - timedelta(days=3)
                    end_date = event_date + timedelta(days=14)

                    if onset_date > end_date or event_date > confirm_date:
                        messages.error(request, "case date out of range")
                        return render(request, 'case_form.html', {'form': form, 'formset': formset})

                messages.success(request, 'You have add the new case successfully!')         
                new_case = form.save()
                new_events = formset.save()
                form = CaseForm()
                for event in new_events:
                    new_case.events.add(event)
            else:
                messages.error(request, 'Wrong date input.' + str(form.cleaned_data['birth']) )
        else:
            messages.error(request, 'There are some data miss, please check.')
    else:
        form = CaseForm()
        formset = eventFormSet(queryset=Event.objects.none())

    return render(request, 'case_form.html', {'form': form, 'formset': formset})

def EventFormView(request):
    startDate = datetime(2020,1,23)
    endDate = datetime.now()

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            startDateDelta = form.cleaned_data['date'] - startDate.date()
            endDateDelta = endDate.date() - form.cleaned_data['date'] 
            if startDateDelta < timedelta(days=0) or endDateDelta < timedelta(days=0):
                messages.error(request, str(form.cleaned_data['date']) + " is out off the covid period in Hong Kong." )
            else:
                cases = form.cleaned_data['cases']
                event_date = form.cleaned_data['date']
                end_date = event_date + timedelta(days=14)
                for case in cases:
                    if case.onset_date > end_date or case.confirm_date < event_date:
                        messages.error(request, "case date out of range")
                new_event = form.save()
                messages.success(request, 'You have add the new event successfully!') 
                form = EventForm()
            # return redirect('test')
        else:
            messages.error(request, 'There are some data miss, please check.')
    else:
        form = EventForm()


    return render(request, 'event_form.html', {'form': form})

def AddAttendanceView(request, add_type, id_num):


    if add_type == 'case':
        data_obj = Case.objects.get(pk = id_num)
    elif add_type == 'event':
        data_obj = Event.objects.get(pk = id_num)

    if request.method == 'POST':
        if add_type == 'case':
            form = EventToCaseForm(request.POST, instance=data_obj)
        elif add_type == 'event':
            form = CaseToEventForm(request.POST, instance=data_obj)
        
        if form.is_valid():
            new_attendance = form.save()
            return redirect('test')

    else:
        if add_type == 'case':
            form = EventToCaseForm(instance=data_obj)
            
            confirm_date = data_obj.confirm_date
            infect_date = data_obj.onset_date - timedelta(days=14)
            valid_events = Event.objects.filter(date__lte=confirm_date)
            valid_events = valid_events.filter(date__gte=infect_date)
            form.fields['events'] = ModelMultipleChoiceField(queryset=valid_events,widget=CheckboxSelectMultiple)
        elif add_type == 'event':
            form = CaseToEventForm(instance=data_obj) 

            event_date = data_obj.date
            end_date = event_date + timedelta(days=14)
            valid_cases = Case.objects.filter(confirm_date__gt=event_date)
            valid_cases = valid_cases.filter(onset_date__lte=end_date)
            form.fields['cases'] = ModelMultipleChoiceField(queryset=valid_cases,widget=CheckboxSelectMultiple)

    return render(request, 'add_attendance_form.html', {'form': form, 'add_type': add_type, 'attendance': data_obj})

class LoginView(TemplateView):
    template_name = 'login.html'

class MainView(TemplateView):
    template_name = 'main.html'

class SearchDateView(TemplateView):
    template_name = 'search_date.html'

class SearchCaseView(TemplateView):
    template_name = 'search_case.html'

def LoginAuthentication(request):
    if request.GET.get('username') == 'adminse' and request.GET.get('password') == 'comp3297':
        return redirect('main')
    else:
        return render(request, 'login.html', { 'message': 'Login Failure!' })

def SearchByDate(request):
    if not Event.objects.exists():
        return render(request, 'search_by_date.html')
    elif not request.GET.get('startDate') and not request.GET.get('endDate'):
        startDate = request.GET.get('startDate')
        endDate = request.GET.get('endDate')
        event_list = Event.objects.all()
        return render(request, 'search_by_date.html', { 'event_list': event_list,  'startDate': startDate, 'endDate': endDate })
    else:
        startDate = request.GET.get('startDate')
        endDate = request.GET.get('endDate')
        if not startDate and Event.objects.exists():
            startDate = Event.objects.order_by('date')[0]
        if not endDate:
            endDate = datetime.now().strftime("%Y-%m-%d")
        event_list = Event.objects.all().filter(date__range=[startDate, endDate])
        return render(request, 'search_by_date.html', { 'event_list': event_list, 'startDate': startDate, 'endDate': endDate })

def SearchByCase(request):
    if not Case.objects.exists():
        return render(request, 'search_by_case.html')
    elif not request.GET.get('caseNum'):
        case_list = Case.objects.all()
        return render(request, 'search_by_case.html', {'case_list': case_list})
    else:
        caseNum = request.GET.get('caseNum')
        case_list = Case.objects.all().filter(case_number=caseNum)
        return render(request, 'search_by_case.html', {'case_list': case_list})