from celery import Celery
import pickle
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
    rf_model = pickle.load(open('./best_model.sav', 'rb'))
    return ("Test")

@celery.task()
def get_prediction(year, forks, has_downloads, has_issues, has_wiki, open_issues_count, size, subscribers_count):
    rf_model = pickle.load(open('./best_model.sav', 'rb'))
    return ( rf_model.predict([[year, forks, has_downloads, has_issues, has_wiki, open_issues_count, size, subscribers_count]])[0] )
