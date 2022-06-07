from django.urls import path

from sofia_weather import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('subscribe/', views.SubscribeUserView.as_view(), name='subscribe'),
]