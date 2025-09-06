from django.urls import path
from . import views

app_name = 'maps'

urlpatterns = [
    path('', views.MapView.as_view(), name='map'),
    path('add/', views.add_polluted_area, name='add_area'),
    path('area/<int:pk>/', views.PollutedAreaDetailView.as_view(), name='area_detail'),
    path('area/<int:pk>/edit/', views.edit_polluted_area, name='edit_area'),
    path('area/<int:pk>/delete/', views.delete_polluted_area, name='delete_area'),
    path('area/<int:area_pk>/report/', views.add_report, name='add_report'),
    path('api/areas/', views.get_polluted_areas_json, name='areas_json'),
]

