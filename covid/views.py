from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from datetime import datetime

# Create your views here.

def test(request):
    return HttpResponse("Hello world")

def CaseFormView(request):
    eventFormSet = modelformset_factory(Event, form = EventForm, extra=1)

    if request.method == 'POST':
        form = CaseForm(request.POST)
        formset = eventFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            messages.success(request, 'You have add the new case successfully!') 
            new_case = form.save()
            new_events = formset.save()
            form = CaseForm()
            for event in new_events:
                new_case.events.add(event)
            # return redirect('test')
        else:
            messages.error(request, 'There are some data miss, please check.')
    else:
        form = CaseForm()
        formset = eventFormSet(queryset=Event.objects.none())

    return render(request, 'case_form.html', {'form': form, 'formset': formset})

def EventFormView(request):

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
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
            start_date = data_obj.onset_date - timedelta(days=4)
            end_date = data_obj.onset_date + timedelta(days=15)
            valid_events = Event.objects.filter(date__gt=start_date).filter(date__lt=end_date)
            form.fields['events'] = ModelMultipleChoiceField(queryset=valid_events,widget=CheckboxSelectMultiple)
        elif add_type == 'event':
            form = CaseToEventForm(instance=data_obj) 
            start_date = data_obj.date + timedelta(days=4)
            end_date = data_obj.date - timedelta(days=15)
            valid_cases = Case.objects.filter(onset_date__gt=end_date).filter(onset_date__lt=start_date)
            form.fields['cases'] = ModelMultipleChoiceField(queryset=valid_cases,widget=CheckboxSelectMultiple)

    return render(request, 'add_attendance_form.html', {'form': form, 'add_type': add_type, 'attendance': data_obj})

class LoginView(TemplateView):
    template_name = 'login.html'

class MainView(TemplateView):
    template_name = 'main.html'

def LoginAuthentication(request):
    user = authenticate(username=request.GET.get('username'), password=request.GET.get('password'))
    if user is not None:
        request.session['id'] = user.username
        request.session.set_expiry(10)
        return redirect('main')
    else:
        return render(request, 'login.html', { 'message': 'Login Failure!' })

def SearchByDate(request):
    if not CheckLoggedIn(request):
        return render(request, 'login.html', { 'message': 'Login First!' })

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
            startDate = datetime.strftime(Event.objects.order_by('date')[0].date, '%Y-%m-%d')
            
        if not endDate:
            endDate = datetime.now().strftime("%Y-%m-%d")
        
        event_list = Event.objects.all().filter(date__range=[startDate, endDate])

        if not request.GET.get('endDate'):
            return render(request, 'search_by_date.html', { 'event_list': event_list, 'startDate': startDate})
        elif not request.GET.get('startDate'):
            return render(request, 'search_by_date.html', { 'event_list': event_list, 'endDate': endDate })
        else:
            return render(request, 'search_by_date.html', { 'event_list': event_list, 'startDate': startDate, 'endDate': endDate })

def SearchByCase(request):
    if not CheckLoggedIn(request):
        return render(request, 'login.html', { 'message': 'Login First!' })

    if not Case.objects.exists():
        return render(request, 'search_by_case.html')
    elif not request.GET.get('caseNum'):
        case_list = Case.objects.all()
        return render(request, 'search_by_case.html', {'case_list': case_list})
    else:
        caseNum = request.GET.get('caseNum')
        case_list = Case.objects.all().filter(case_number=caseNum)
        return render(request, 'search_by_case.html', {'case_list': case_list, 'caseNum': caseNum})

def CheckLoggedIn(request):
    try:
        if User.objects.get(username=request.session.get('id')) is not None:
            return True
    except:
        return False