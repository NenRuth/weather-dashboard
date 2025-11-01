from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search/', views.search_weather, name='search_weather'),
    path('chart/temp-trend/<str:city_name>/', views.temperature_trend, name='temperature_trend'),
]