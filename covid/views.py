from django.shortcuts import render, redirect
from django.http import HttpResponse
from covid.models import *
from django.forms import modelformset_factory
# Create your views here.

def test():
    return HttpResponse("Hello world")



def CaseFormView(request):
    eventFormSet = modelformset_factory(Event, form = EventForm, extra=1)

    if request.method == 'POST':
        form = CaseForm(request.POST)
        formset = eventFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            new_case = form.save()
            new_events = formset.save()
            for event in new_events:
                Attendance.objects.create(case=new_case, event=event)
            return redirect('test')
    else:
        form = CaseForm()
        formset = eventFormSet(queryset=Event.objects.none())
    
    return render(request, 'case_form.html', {'form': form, 'formset': formset})