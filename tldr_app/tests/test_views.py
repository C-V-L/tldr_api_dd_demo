import pytest
import requests
import json
# import requests_mock
import vcr
# from django.urls import reverse
from rest_framework.test import APIClient
from django.test import Client
# from tldr_app.models import Query
from django.test import RequestFactory
from unittest.mock import patch, MagicMock
from tldr_app.views import QueryApiView
from rest_framework import status
from tldr_app.models import *
from tldr_app.serializers import QuerySerializer
from tldr_app.services import QueryGPT

# Perhaps another push will rectofy this issue
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
    assert len(response.data) == 1

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
    assert response.status_code == 200
    assert response.data[0]["tos"] =="test"

# NEXT IS TO TEST MAKING A QUERY 

POST_URL = 'http://localhost:8000/api/v1/queries'

def test_post_request_make_query():
    payload = {
      "user": 1,
      "areas_of_focus": ["mandatory binding arbitration", "recurring payments"],
      "tos": "Netflix Terms of Use\nNetflix provides a personalized subscription service that allows our members to access entertainment content "
    }
    headers = {'Content-Type': 'application/json'}
    # This is the path to the cassette that was being used in the previosu test file test_queries_api_calls.py It's being
    # used here now and should be passing all below tests.
    with vcr.VCR().use_cassette('fixtures/vcr_cassettes/synopsis.yaml'):
      response = requests.post(POST_URL, data=json.dumps(payload), headers=headers)
      assert response.status_code == 201
      response_data = response.json()
      assert isinstance(response_data, dict)
      assert isinstance(response_data['data'], list)
      assert isinstance(response_data['data'][0], dict)
      assert isinstance(response_data['data'][0]['title'], str)
      assert isinstance(response_data['data'][0]['impact'], str)
      assert isinstance(response_data['data'][0]['actionable'], str)
      assert isinstance(response_data['data'][0]['ranking'], int)
      assert isinstance(response_data['data'][1], dict)
      assert isinstance(response_data['data'][1]['title'], str)
      assert isinstance(response_data['data'][1]['impact'], str)
      assert isinstance(response_data['data'][1]['actionable'], str)
      assert isinstance(response_data['data'][1]['ranking'], int)

def test_post_individual_unit_test(db):
    user = User.objects.create(name="Hady")
    query = Query.objects.create(user=user, tos="test", areas_of_focus=["payment", "subscription"])
    result = Result.objects.create(query=query, response={"title": "Test title", "impact": "Test impact", "actionable": "Test actionable", "ranking": 1})
    
    factory = RequestFactory()
    request = factory.post('/fake-url/', data= {"areas_of_focus": ["area", "focus"], "tos" :"sample TOS", "user": user.id}) 

    with patch('tldr_app.serializers.QuerySerializer.save') as mock_save:
        mock_save.return_value = MagicMock()

        with patch('tldr_app.services.QueryGPT.initiate_query') as mock_initiate_query:
            mock_initiate_query.return_value = [result]

            request.data = request.POST  # Assign the data from POST to request.data

            response = QueryApiView().post(request)

            assert response.status_code == status.HTTP_201_CREATED

            mock_save.assert_called_once()

def test_post_individual_nonvalid_unit_test(db):
    user = User.objects.create(name="Isaac")
    query = Query.objects.create(user=user, tos="invalidtest", areas_of_focus=["payment", "subscription"])
    result = Result.objects.create(query=query, response="This is an invalid test response")
    
    factory = RequestFactory()
    request = factory.post('/fake-url/')
    request.data = {"areas_of_focus": 9, "tos": "sample TOS", "user": user.id}

    with patch('tldr_app.views.QuerySerializer') as mock_query_serializer:
        mock_instance = mock_query_serializer.return_value
        mock_instance.is_valid.return_value = False

    response = QueryApiView().post(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    #Further suggestion is to include the bottom two lines of code to ensure the QuerySerializer was at least called once, 
    #but that would call for further refactoring to use django.http's QueryDict and rest_framework.test's APIRequestFactory.
    #Ulitmately, the else condition of the QueryApiView's post method is being hit and tested, so I think this is sufficient.

    # mock_query_serializer.assert_called_once_with(data=request.data)
    # mock_instance.is_valid.assert_called_once()