from django.urls import path
from weather_app import views

app_name = 'weather_app'
urlpatterns = [
    # My urls
    path('', views.index, name="index"),
    path('weekly_forecast/', views.weekly_forecast, name="weekly_forecast"),
    path('comment/', views.comment, name="comment"),
    path('attributions/', views.attributions, name="attrib"),
    path('set_temp_units/<str:units>/', views.set_temp_units, name="set_temp_units")
]
