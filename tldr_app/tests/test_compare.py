import vcr
from rest_framework.test import APIClient, APITestCase
from tldr_app.models import *

class CompareTest(APITestCase):
		def setUp(self):
			self.client = APIClient()

		def test_post_compare(self):
			user = User.objects.create(name="Hady", id=1)
			url = 'http://localhost:8000/api/v1/compare'
			payload = {
				"user": user.id,
				"areas_of_focus": ["mandatory binding arbitration", "recurring payments"],
				"tos1": "Netflix Terms of Use\nNetflix provides a personalized subscription service that allows our members to access entertainment content ",
				"tos2": "Apple Terms of Use\Apple provides a subscription based service that allows our members to access audio content "
			}
			
			my_vcr = vcr.VCR(
    		filter_headers=['Authorization'],
				)
			with my_vcr.use_cassette('fixtures/vcr_cassettes/json_compare1.yaml'):
				response = self.client.post(url, payload, format='json')
				assert response.status_code == 201
				response_data = response.json()
				assert isinstance(response_data, dict)
				assert isinstance(response_data['title'], str)
				assert isinstance(response_data['company_1'], str)
				assert isinstance(response_data['company_2'], str)
				assert isinstance(response_data['comparison'], str)