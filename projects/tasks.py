import logging
 
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from Brands.celery import app
from .twitter2 import Twitter
from .misc import temp
 
 
@app.task
def temp_task(search_query, number, filename, result_type):
    t = Twitter(search_query, number, filename, result_type)
    t.rest()
    
    print("Task executed! Horray..." + search_query)

@app.task
def stream_task(search_query, number, filename, result_type):
    t = Twitter(search_query, number, filename, result_type)
    t.livestream()
    
    print("Task executed! Horray..." + search_query)
