from tldr_app.services import QueryGPT
from celery import shared_task

@shared_task
def query(query):
    QueryGPT.initiate_query(query)