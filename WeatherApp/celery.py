import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeatherApp.settings')

app = Celery('WeatherApp')
app.conf.enable_utc = False

app.conf.update(timezone='Europe/Sofia')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'send_weather_to_client_every_day': {
        'task': 'sofia_weather.tasks.send_weather_email_task',
        'schedule': crontab(hour=19, minute=7),
    },
    'send_mail_screenshot_every_day': {
        'task': 'sofia_weather.tasks.send_screenshot_email_task',
        'schedule': crontab(hour=18, minute=25),
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
