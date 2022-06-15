from datetime import datetime, timedelta

from django.contrib.sites import requests
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from api_weatherapp.serializers import SubscribedUsersSerializer


class WeatherView(APIView):
    name = 'Weather'

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
    name = 'subscribe'
    serializer_class = SubscribedUsersSerializer



