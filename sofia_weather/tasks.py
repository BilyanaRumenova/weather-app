from datetime import datetime, timedelta
from time import sleep

import requests
from celery.utils.log import get_task_logger
from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template

from WeatherApp import settings
from sofia_weather.models import SubscribedUsers

logger = get_task_logger(__name__)


@shared_task
def send_email_after_subscription_task(email, name):
    email = SubscribedUsers.objects.get(email=email)

    mail_subject = "Test Celery"
    link = 'http://127.0.0.1:8000'
    message = f'Hello, {name}!\n' \
              f' Thank you for subscription!\n' \
              f'You can check the current weather in Sofia here: {link}'
    to_email = email
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email, ]
    )

    logger.info('Sent email successfully!')
    return 'Done'


@shared_task
def send_periodic_email_task():
    subscribers = SubscribedUsers.objects.all()

    for subscriber in subscribers:
        email = subscriber.email
        name = subscriber.name

        subject = 'Welcome to Sofia Weather'
        message = f'Hello {name}!\n' \
                  f'Here is your weather forecast'
        to_email = email
        recipient_list = [to_email, ]
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=True
        )

    logger.info('Mail sending.......')
    return 'Periodic task sent'


@shared_task
def send_weather_email_task():
    subscribers = SubscribedUsers.objects.all()

    for subscriber in subscribers:
        email = subscriber.email
        name = subscriber.name

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

        subject = 'Welcome to Sofia Weather'
        message = get_template('email/email_weather.html').render(context)

        to_email = email
        recipient_list = [to_email, ]
        msg = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list,
        )
        msg.content_subtype = "html"
        msg.send()

# @shared_task
# def send_weather_email_task():
#     subscribers = SubscribedUsers.objects.all()
#
#     for subscriber in subscribers:
#         email = subscriber.email
#         name = subscriber.name
#
#         city = 'Sofia'
#         city_lat = '42.6951'
#         city_lon = '23.325'
#         API_key = '24eede1f3b0f51f76e7f4597fbf3fc1b'
#         source_url = f'https://api.openweathermap.org/data/2.5/' \
#                      f'onecall?lat={city_lat}&lon={city_lon}&units=metric&appid={API_key}'
#
#         city_weather = requests.get(source_url).json()
#
#         current_weather = {
#             'city': city,
#             'temperature': city_weather['current']['temp'],
#             'feels_like': city_weather['current']['feels_like'],
#             'humidity': city_weather['current']['humidity'],
#             'description': city_weather['current']['weather'][0]['description'],
#             'weather_icon': city_weather['current']['weather'][0]['icon'],
#             'min_temp': city_weather['daily'][0]['temp']['min'],
#             'max_temp': city_weather['daily'][0]['temp']['max'],
#             'date': datetime.now(),
#         }
#
#         weather_weekly = {
#             'daily_forecast': city_weather['daily'][1:],
#         }
#
#         for day in weather_weekly.values():
#             days = 1
#             for d in day:
#                 current_time_date = datetime.now() + timedelta(days=days)
#                 current_time = current_time_date.strftime('%A, %d %b, %Y')
#                 d.update({'date': current_time})
#                 days += 1
#
#         context = {
#             'current_weather': current_weather,
#             'weather_weekly': weather_weekly,
#         }
#
#         subject = 'Welcome to Sofia Weather'
#         message = get_template('email/email_weather.html').render(context)
#
#         to_email = email
#         recipient_list = [to_email, ]
#         msg = EmailMessage(
#             subject=subject,
#             body=message,
#             from_email=settings.EMAIL_HOST_USER,
#             to=recipient_list,
#         )
#         msg.content_subtype = "html"
#         msg.send()


@shared_task
def test_func():
    for i in range(10):
        sleep(1)
        print(i)
    return "Done"