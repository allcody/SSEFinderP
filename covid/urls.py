from django.urls import path 
from covid import views

urlpatterns = [
    path('test', views.test),
]