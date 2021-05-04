from django.urls import path 
from covid import views

urlpatterns = [
    path('', views.test, name='test'), 
    path('test', views.test, name='test'),
    path('caseForm', views.CaseFormView, name='case-form'),
    path('eventForm', views.EventFormView, name='event-form'),
    path('addAttendance/<str:add_type>/<int:id_num>', views.AddAttendanceView, name='add-attendance'),
    path('search_case', views.search_case.as_view(), name="search_case"),
    path('search_date', views.search_date.as_view(), name="search_date"),
    path('main', views.main.as_view(), name="main")
]