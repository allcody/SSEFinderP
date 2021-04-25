from django.db import models
from django.forms import ModelForm, modelformset_factory, ModelMultipleChoiceField, SelectMultiple, CheckboxSelectMultiple
# Create your models here.

class Event(models.Model):
    venue_name = models.CharField(max_length=200)
    venue_location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    x_coordinate = models.DecimalField(max_digits=10, decimal_places=3)
    y_coordinate = models.DecimalField(max_digits=10, decimal_places=3)
    date = models.DateTimeField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.venue_name

class Case(models.Model):
    case_number = models.CharField(max_length=200)
    person_name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=200)
    birth = models.DateTimeField()
    onset_date = models.DateTimeField()
    confirm_date = models.DateTimeField()

    def __str__(self):
        return self.case_number

class Attendance(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.case) + " " +str(self.event)

class CaseForm(ModelForm):
    event_select = ModelMultipleChoiceField(Event.objects, widget=CheckboxSelectMultiple, required=False)

    class Meta:
        model = Case
        fields = ['case_number', 'person_name', 'id_number', 'birth', 'onset_date', 'confirm_date']

    def save(self):
        new_case_data = self.cleaned_data.copy()
        del new_case_data['event_select']
        new_case = Case.objects.create(**new_case_data)

        for event in self.cleaned_data['event_select']:
            Attendance.objects.create(case=new_case, event=event)

        return new_case

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['venue_name', 'venue_location', 'address', 'x_coordinate', 'y_coordinate', 'date', 'description']
