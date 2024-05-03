from celery import shared_task
import time


@shared_task(bind=True)
def test_func(self):
    print('-------------> TASK')
    return "Done"


@shared_task
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True
