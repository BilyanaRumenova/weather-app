from time import sleep
from celery.utils.log import get_task_logger
from celery import shared_task

from sofia_weather.email import send_email_after_subscription

logger = get_task_logger(__name__)


@shared_task
def send_email_after_subscription_task():
    logger.info('Sent email successfully!')
    return 'Done'


@shared_task
def test_func():
    for i in range(10):
        sleep(1)
        print(i)
    return "Done"