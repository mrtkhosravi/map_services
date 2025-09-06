from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('my-areas/', views.my_areas, name='my_areas'),
    path('my-reports/', views.my_reports, name='my_reports'),
]

