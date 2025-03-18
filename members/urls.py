from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('duty_roster/', views.duty_roster, name='duty_roster'),
    path('instructors/', views.instructors_only, name='instructors'),
    path('members/', views.members_list, name='members'),
    path('log_sheets/', views.log_sheets, name='log_sheets'),
]

