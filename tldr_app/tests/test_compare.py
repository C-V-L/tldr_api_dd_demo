import requests
import json
import vcr
from rest_framework.test import APIClient
from django.test import RequestFactory
from unittest.mock import patch, MagicMock
from tldr_app.views import QueryApiView
from rest_framework import status
from tldr_app.models import *

# NEXT IS TO TEST MAKING A QUERY 

POST_URL = 'http://localhost:8000/api/v1/compare'

my_vcr = vcr.VCR(
    filter_headers=['Authorization'],
)

def test_post_compare(db):
    User.objects.create(name="Hady")
    payload = {
			"user": 1,
			"areas_of_focus": ["mandatory binding arbitration", "recurring payments"],
			"tos1": "Netflix Terms of Use\nNetflix provides a personalized subscription service that allows our members to access entertainment content ",
			"tos2": "Spotify Terms of Use\Spotify provides a subscription based service that allows our members to access audio content "
		}
    
    headers = {'Content-Type': 'application/json'}
    
    with my_vcr.use_cassette('fixtures/vcr_cassettes/json_compare.yaml'):
      response = requests.post(POST_URL, data=json.dumps(payload), headers=headers)
      assert response.status_code == 201
      response_data = response.json()
      assert isinstance(response_data, dict)
      assert isinstance(response_data['title'], str)
      assert isinstance(response_data['company_1'], str)
      assert isinstance(response_data['company_2'], str)
      assert isinstance(response_data['comparison'], str)