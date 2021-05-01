from django.urls import path 
from covid import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('caseForm', views.CaseFormView, name='case-form'),
    path('eventForm', views.EventFormView, name='event-form'),
<<<<<<< HEAD
    path('addAttendance/<str:add_type><int:id_num>', views.AddAttendanceView, name='add-attendance'),
    path('login', views.login)
=======
    path('addAttendance/<str:add_type><int:id_num>', views.AddAttendanceView, name='add-attendance')
>>>>>>> refs/remotes/origin/main
]