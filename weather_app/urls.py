from django.urls import path
from weather_app import views

app_name = 'weather_app'
urlpatterns = [
    # My urls
    path('', views.index, name="index"),
    path('weekly_forecast/', views.weekly_forecast, name="weekly_forecast")
]
