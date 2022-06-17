from django.urls import path

from api_weatherapp import views

urlpatterns = [
    path('', views.WeatherView.as_view()),
    path('subscribe/', views.SubscribeView.as_view()),
    path('task/<str:task_id>/', views.TaskView.as_view(), name='task'),
]