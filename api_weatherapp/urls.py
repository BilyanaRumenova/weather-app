from django.urls import path

from api_weatherapp import views
from api_weatherapp.views import SubscribeView

urlpatterns = [
    path('', views.WeatherView.as_view(), name=views.WeatherView.name),
    path('subscribe/', SubscribeView.as_view(), name=views.SubscribeView.name)
]