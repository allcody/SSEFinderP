from django.db import models

# Create your models here.

class Evnet(models.Model):
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
