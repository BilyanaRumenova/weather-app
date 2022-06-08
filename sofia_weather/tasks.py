from time import sleep

from celery import shared_task


@shared_task
def test_func():
    for i in range(10):
        sleep(1)
        print(i)
    return "Done"