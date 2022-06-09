from time import sleep
from celery.utils.log import get_task_logger
from celery import shared_task
from django.core.mail import send_mail

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
def test_func():
    for i in range(10):
        sleep(1)
        print(i)
    return "Done"