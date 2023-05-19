import pytest
import requests
import json
# import requests_mock
import vcr

POST_URL = 'http://localhost:8000/api/v1/queries'

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
      assert response_data['data'][0].keys() == {'title', 'impact', 'actionable', 'ranking'}
      assert isinstance(response_data['data'][0], dict)
      assert isinstance(response_data['data'][0], dict)
      assert isinstance(response_data['data'][0]['title'], str)
      assert isinstance(response_data['data'][0]['impact'], str)
      assert isinstance(response_data['data'][0]['actionable'], str)
      assert isinstance(response_data['data'][0]['ranking'], int)

# def test_get_request(): 
#     with vcr.VCR().use_cassette('fixtures/vcr_cassettes/get_synopsis.yaml'):
#       response = requests.get(BASE_URL)