from django.urls import path 
from covid import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('caseForm', views.CaseFormView, name='case-form'),
    path('eventForm', views.EventFormView, name='event-form')
]