import vcr
from rest_framework.test import APIClient, APITestCase
from tldr_app.models import *
from django.core.files.uploadedfile import SimpleUploadedFile

class CompareTest(APITestCase):
		def setUp(self):
			self.client = APIClient()
			self.user = User.objects.create(name="Hady", id=1)

		def test_post_compare(self):
			url = 'http://localhost:8000/api/v1/compare'
			payload = {
				"user": self.user.id,
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

		def test_post_compare_pdf(self):
			url = 'http://localhost:8000/api/v1/compare'
			with open('tldr_app/tests/spotify.pdf', 'rb') as f1, open('tldr_app/tests/netflix.pdf', 'rb') as f2:
				data = {
					'file1': f1, 
					'file2': f2, 
					'user': self.user.id
					}
			
				my_vcr = vcr.VCR(
					filter_headers=['Authorization'],
					)
				with my_vcr.use_cassette('fixtures/vcr_cassettes/pdf_compare.yaml'):
					response = self.client.post(url, data, format='multipart')
					assert response.status_code == 201
					response_data = response.json()
					assert isinstance(response_data, dict)
					assert isinstance(response_data['title'], str)
					assert isinstance(response_data['company_1'], str)
					assert isinstance(response_data['company_2'], str)
					assert isinstance(response_data['comparison'], str)

		def test_post_compare_no_user(self):
			url = 'http://localhost:8000/api/v1/compare'
			with open('tldr_app/tests/spotify.pdf', 'rb') as f1, open('tldr_app/tests/netflix.pdf', 'rb') as f2:
				data = {
					'file1': f1, 
					'file2': f2, 
					}

				response = self.client.post(url, data, format='multipart')
				assert response.status_code == 400

		def test_post_compare_error(self):
			url = 'http://localhost:8000/api/v1/compare'
			with open('tldr_app/tests/spotify.pdf', 'rb') as f1, open('tldr_app/tests/netflix.pdf', 'rb') as f2:
				data = {
						'user': 1
					}
			
				response = self.client.post(url, data, format='multipart')
				assert response.status_code == 400