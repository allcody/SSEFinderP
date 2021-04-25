from django.db import models
from django.forms import ModelForm, modelformset_factory, ModelMultipleChoiceField, SelectMultiple, CheckboxSelectMultiple, TextInput, DateInput
# Create your models here.

class Attendance(models.Model):
    case = models.ForeignKey('Case', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.case)} attended {str(self.event)}'

class Event(models.Model):
    venue_name = models.CharField(max_length=200)
    venue_location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    x_coordinate = models.DecimalField(max_digits=10, decimal_places=3)
    y_coordinate = models.DecimalField(max_digits=10, decimal_places=3)
    date = models.DateField()
    description = models.CharField(max_length=200)
    cases = models.ManyToManyField('Case', through=Attendance)

    def __str__(self):
        return f'{self.venue_name} {self.date}'

class Case(models.Model):
    case_number = models.CharField(max_length=200)
    person_name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=200)
    birth = models.DateField()
    onset_date = models.DateField()
    confirm_date = models.DateField()
    events = models.ManyToManyField('Event', through=Attendance)

    def __str__(self):
        return self.case_number



class DateInput(DateInput):
    input_type = 'date'

class CaseForm(ModelForm):

    class Meta:
        model = Case
        fields = ['case_number', 'person_name', 'id_number', 'birth', 'onset_date', 'confirm_date', 'events']
        widgets = {
            'birth' : DateInput(),
            'onset_date' : DateInput(),
            'confirm_date' : DateInput(),
            'events' : CheckboxSelectMultiple
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['venue_location', 'venue_name', 'address', 'x_coordinate', 'y_coordinate', 'date', 'description']
        widgets = {
            # 'address' : TextInput(attrs={'readonly':True}),
            # 'venue_name' : TextInput(attrs={'readonly':True}),
            # 'x_coordinate' : TextInput(attrs={'readonly':True}),
            # 'y_coordinate' : TextInput(attrs={'readonly':True}),
            'date' : DateInput()
        }


class EventToCaseForm(ModelForm):
    class Meta:
        model = Case
        fields = ['case_number', 'person_name', 'onset_date', 'confirm_date', 'events']

        widgets = {
            'case_number' : TextInput(attrs={'readonly':True}),
            'person_name' : TextInput(attrs={'readonly':True}),
            'onset_date' : TextInput(attrs={'readonly':True}),
            'confirm_date' : TextInput(attrs={'readonly':True}),
            'events' : CheckboxSelectMultiple
        }

class CaseToEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['venue_location', 'venue_name', 'address', 'x_coordinate', 'y_coordinate', 'date', 'description', 'cases']
        widgets = {
            'address' : TextInput(attrs={'readonly':True}),
            'venue_name' : TextInput(attrs={'readonly':True}),
            'venue_location' : TextInput(attrs={'readonly':True}),
            'x_coordinate' : TextInput(attrs={'readonly':True}),
            'y_coordinate' : TextInput(attrs={'readonly':True}),
            'date' : TextInput(attrs={'readonly':True}),
            'description' : TextInput(attrs={'readonly':True}),
            'cases' : CheckboxSelectMultiple
        }