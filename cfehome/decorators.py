import functools
import logging

from celery import shared_task
from django.db import transaction

logger = logging.getLogger('django')


class custom_celery_task:
    """
    This is a decorator we can use to add custom logic to our Celery task
    such as retry or database transaction
    """

    def __init__(self, *args, **kwargs):
        self.task_args = args
        self.task_kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                with transaction.atomic():
                    return func(*args, **kwargs)
            except Exception as e:
                logger.error(f'task failed : {e}')
                # task_func.request.retries
                raise task_func.retry(exc=e, countdown=5)

        task_func = shared_task(*self.task_args, **self.task_kwargs)(wrapper_func)
        return task_func



# @custom_celery_task(max_retries=5)
# def task_transaction_test():
#     # do something