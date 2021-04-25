from django.db import models
from django.forms import ModelForm, modelformset_factory, ModelMultipleChoiceField, SelectMultiple, CheckboxSelectMultiple, TextInput, DateInput
# Create your models here.

class Event(models.Model):
    venue_name = models.CharField(max_length=200)
    venue_location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    x_coordinate = models.DecimalField(max_digits=10, decimal_places=3)
    y_coordinate = models.DecimalField(max_digits=10, decimal_places=3)
    date = models.DateField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.venue_name} {self.date}'

class Case(models.Model):
    case_number = models.CharField(max_length=200)
    person_name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=200)
    birth = models.DateField()
    onset_date = models.DateField()
    confirm_date = models.DateField()
    events = models.ManyToManyField(Event)

    def __str__(self):
        return self.case_number

        
class DateInput(DateInput):
    input_type = 'date'

class CaseForm(ModelForm):
    # event_select = ModelMultipleChoiceField(Event.objects, widget=CheckboxSelectMultiple, required=False)

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
