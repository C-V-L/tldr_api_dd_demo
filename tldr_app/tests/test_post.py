# import pytest
import requests
import json

BASE_URL = 'http://localhost:8000/api/queries'

def test_post_request():
    payload = {
      "user": 1,
      "areas_of_focus": ["mandatory binding arbitration", "recurring payments"],
      "tos": "Netflix Terms of Use\nNetflix provides a personalized subscription service that allows our members to access entertainment content "
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(BASE_URL, data=json.dumps(payload), headers=headers)
    assert response.status_code == 201
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert isinstance(response_data['response'], str)