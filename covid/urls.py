from django.urls import path 
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('fetchLoginData', views.LoginAuthentication, name='fetch_login_data'),
<<<<<<< Updated upstream
    path('covid', views.MainView.as_view(), name='main'),
    path('searchCase', views.SearchByCase, name='search_case'),
    path('searchDate', views.SearchByDate, name='search_date'),
=======
    path('main', views.Main, name='main'),
    path('searchCase', views.SearchByCase, name='search_by_case'),
    path('searchDate', views.SearchByDate, name='search_by_date'),
>>>>>>> Stashed changes

    path('test', views.test, name='test'),
    path('caseForm', views.CaseFormView, name='case-form'),
    path('eventForm', views.EventFormView, name='event-form'),
    path('addAttendance/<str:add_type><int:id_num>', views.AddAttendanceView, name='add-attendance')
]