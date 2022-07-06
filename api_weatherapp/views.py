from datetime import datetime, timedelta

from django.contrib.sites import requests
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from api_weatherapp.serializers import SubscribedUsersSerializer
from celery_utils.tasks import send_email_after_subscription_task
from celery import current_app


class WeatherView(APIView):

    def get(self, request):

        city = 'Sofia'
        city_lat = '42.6951'
        city_lon = '23.325'
        API_key = '24eede1f3b0f51f76e7f4597fbf3fc1b'
        source_url = f'https://api.openweathermap.org/data/2.5/' \
                     f'onecall?lat={city_lat}&lon={city_lon}&units=metric&appid={API_key}'

        city_weather = requests.get(source_url).json()

        current_weather = {
            'city': city,
            'temperature': city_weather['current']['temp'],
            'feels_like': city_weather['current']['feels_like'],
            'humidity': city_weather['current']['humidity'],
            'description': city_weather['current']['weather'][0]['description'],
            'weather_icon': city_weather['current']['weather'][0]['icon'],
            'min_temp': city_weather['daily'][0]['temp']['min'],
            'max_temp': city_weather['daily'][0]['temp']['max'],
            'date': datetime.now(),
        }

        weather_weekly = [city_weather['daily'][1:]]

        weekly_forecast = {}
        daily = []
        for day in weather_weekly:
            days = 1

            for d in day:
                current_time_date = datetime.now() + timedelta(days=days)
                current_time = current_time_date.strftime('%A, %d %b, %Y')
                weekly_forecast['temperature'] = d['temp']['day']
                weekly_forecast['forecast_icon'] = d['weather'][0]['icon']
                weekly_forecast['description'] = d['weather'][0]['description']
                weekly_forecast['min_temperature'] = d['temp']['min']
                weekly_forecast['max_temperature'] = d['temp']['max']
                weekly_forecast['date'] = current_time
                daily.append(weekly_forecast)
                weekly_forecast = {}
                days += 1

        context = {
            'current_weather': current_weather,
            'weekly_forecast': daily,
        }

        return Response(context)


class SubscribeView(CreateAPIView):
    serializer_class = SubscribedUsersSerializer

    def post(self, request, *args, **kwargs):
        subscriber_serializer = SubscribedUsersSerializer(data=request.data)
        if subscriber_serializer.is_valid():
            subscriber_serializer.save()
            subscriber_name = request.data['name']
            subscriber_email = request.data['email']
            send_email_after_subscription_task.delay(subscriber_email, subscriber_name)
            return Response(subscriber_serializer.data, status=status.HTTP_201_CREATED)
        return Response(subscriber_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskView(APIView):
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {
            'task_status': task.status,
            'task_id': task.id,
            'date_done': task.date_done,
        }

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return Response(response_data)


