from datetime import datetime, timedelta

from django.shortcuts import render
import requests
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from sofia_weather.forms import SubscribedUsersForm
from sofia_weather.tasks import send_email_after_subscription_task


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
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

        weather_weekly = {
            'daily_forecast': city_weather['daily'][1:],
        }

        for day in weather_weekly.values():
            days = 1
            for d in day:
                current_time_date = datetime.now() + timedelta(days=days)
                current_time = current_time_date.strftime('%A, %d %b, %Y')
                d.update({'date': current_time})
                days += 1

        context = {
            'current_weather': current_weather,
            'weather_weekly': weather_weekly,
        }
        return context


class SubscribeUserView(FormView):
    form_class = SubscribedUsersForm
    template_name = 'subscribe/subscribe.html'
    success_url = reverse_lazy('subscribe')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        subscriber = form.save(commit=False)
        subscriber.save()
        is_subscribed = True
        email = subscriber.email
        name = subscriber.name
        send_email_after_subscription_task.delay(email, name)

        context = {
            'is_subscribed': is_subscribed
        }
        return render(self.request, 'subscribe/subscribe.html', context)


