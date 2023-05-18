import pytest
import requests
import json
# import requests_mock
import vcr
# from django.urls import reverse
from rest_framework.test import APIClient
from django.test import Client
from tldr_app.models import User, Query

client = APIClient()

def test_health_check_view():
    url = 'http://localhost:8000/healthcheck'
    response = client.get(url)
    assert response.status_code == 200

def test_get_all_users(db): 
    User.objects.create(name="Hady")
    url = 'http://localhost:8000/api/v1/users'
    response = client.get(url)
    assert response.status_code == 200
    assert response.data[0]["name"] == "Hady"

def test_create_user(db):
    url = 'http://localhost:8000/api/v1/users'
    user_data = {'name': 'Hady'}
    response = client.post(url, data=user_data)
    assert response.status_code == 201
    assert response.data['name'] == 'Hady'

def test_user_sad_path_empty(db):
    url = 'http://localhost:8000/api/v1/users'
    user_data = {'name': ''}
    response = client.post(url, data=user_data)
    assert response.status_code == 400

def test_get_all_queries(db):
    user = User.objects.create(name="Hady")
    Query.objects.create(user=user, tos="test", areas_of_focus=["payment", "subscription"])
    url = 'http://localhost:8000/api/v1/queries'
    response = client.get(url)
    breakpoint()
    assert response.status_code == 200
    assert response.data[0]["tos"] =="test"

# NEXT IS TO TEST MAKING A QUERY 

POST_URL = 'http://localhost:8000/api/queries'

def test_post_request():
    payload = {
      "user": 1,
      "areas_of_focus": ["mandatory binding arbitration", "recurring payments"],
      "tos": "Netflix Terms of Use\nNetflix provides a personalized subscription service that allows our members to access entertainment content "
    }
    headers = {'Content-Type': 'application/json'}

    with vcr.VCR().use_cassette('fixtures/vcr_cassettes/synopsis.yaml'):
      response = requests.post(POST_URL, data=json.dumps(payload), headers=headers)
      assert response.status_code == 201
      response_data = response.json()
      assert isinstance(response_data, dict)
      assert isinstance(response_data['response'], str)
      assert isinstance(response_data['id'], int)

# def test_get_request(): 
#     with vcr.VCR().use_cassette('fixtures/vcr_cassettes/get_synopsis.yaml'):
#       response = requests.get(BASE_URL)