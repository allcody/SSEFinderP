from django.shortcuts import render, redirect
from django.http import HttpResponse
from covid.models import *
from django.forms import modelformset_factory, TextInput, CheckboxSelectMultiple
from django.contrib import messages
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
        elif add_type == 'event':
            form = CaseToEventForm(instance=data_obj) 

    return render(request, 'add_attendance_form.html', {'form': form, 'add_type': add_type, 'attendance': data_obj})
