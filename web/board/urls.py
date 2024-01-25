from django.urls import path
from . import views

from .views import (AccidentCreateView, AccidentListView, AccidentDetailView
                    ,AccidentUpdateView,AccidentDeleteView
                    , SafetyListView, SafetyCreateView, SafetyDetailView
                    , SafetyDeleteView, SafetyUpdateView, LogView, FieldlogView, FieldlogDetailView
                    , FieldlogDeleteView, FieldlogUpdateView, PreferencesView, EmployeeView
                    , EmployeeUpdateView, EmployeeDeleteView, GroupView, GroupDeleteView, DashboardView)

app_name = "board"

urlpatterns = [
    path('login/', views.Login, name="login"),
    path('logout/', views.Logout, name="logout"),
    path('signup/', views.Signup, name="signup"),
    path('log/', LogView.as_view(), name='log'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/<int:pk>/', DashboardView.as_view(), name='dashboard_detail'),
    path('accident_write/', AccidentCreateView.as_view(), name='accident_write'),
    path('accident_list/', AccidentListView.as_view(), name='accident_list'),
    path('accident_detail/<int:pk>/', AccidentDetailView.as_view(), name='accident_detail'),
    path('accident_update/<int:pk>/', AccidentUpdateView.as_view(), name='accident_update'),
    path('accident_delete/<int:pk>/', AccidentDeleteView.as_view(), name="accident_delete"),
    path('safety_write/', SafetyCreateView.as_view(), name='safety_write'),
    path('safety_list/', SafetyListView.as_view(), name='safety_list'),
    path('safety_detail/<int:pk>/', SafetyDetailView.as_view(), name='safety_detail'),
    path('safety_update/<int:pk>/', SafetyUpdateView.as_view(), name='safety_update'),
    path('safety_delete/<int:pk>/', SafetyDeleteView.as_view(), name="safety_delete"),
    path('fieldlog_write/', FieldlogView.as_view(), name='fieldlog_write'),
    path('fieldlog_detail/<int:pk>/', FieldlogDetailView.as_view(), name='fieldlog_detail'),
    path('fieldlog_update/<int:pk>/', FieldlogUpdateView.as_view(), name='fieldlog_update'),
    path('fieldlog_delete/<int:pk>/', FieldlogDeleteView.as_view(), name='fieldlog_delete'),
    path('preferences/', PreferencesView.as_view(), name="preferences_list"),
    path('preferences/<int:pk>/', PreferencesView.as_view(), name="preferences_detail"),
    path('employee/', EmployeeView.as_view(), name="employee"),
    path('employee_detail/<int:pk>/', EmployeeView.as_view(), name='employee_detail'),
    path('employee_update/<int:pk>/', EmployeeUpdateView.as_view(), name="employee_update"),
    path('employee_delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('groups/', GroupView.as_view(), name='groups'),
    path('groups_delete/<int:pk>', GroupDeleteView.as_view(), name='groups_delete'),
    # path('profile/', profile, name='profile'),
    path('apimap/', views.Apimap, name="apimap"),
]