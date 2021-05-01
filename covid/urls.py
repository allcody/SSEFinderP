from django.urls import path 
from covid import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('caseForm', views.CaseFormView, name='case-form'),
    path('eventForm', views.EventFormView, name='event-form'),
    path('addAttendance/<str:add_type><int:id_num>', views.AddAttendanceView, name='add-attendance')
]