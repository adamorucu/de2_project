from celery import Celery

from numpy import loadtxt
import numpy as np

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('worker', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task()
def add_nums():
    a= 2
    b = 3
   return a + b
