# import pytest
# import requests
# import json
# import vcr
# from rest_framework.test import APIClient
# from django.test import Client
from tldr_app.models import User
from tldr_app.serializers import QuerySerializer

def test_query_serializer(db):
    random_user = User.objects.create(name="Hady")
    request_data= {"areas_of_focus":["area", "focus"], "tos" :"sample TOS", "user": random_user.id} 
    serialized = QuerySerializer(data=request_data)
    assert serialized.is_valid()