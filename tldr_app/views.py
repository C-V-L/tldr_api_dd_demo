from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import *
from .serializers import UserSerializer, QuerySerializer, ResultSerializer
from .renderers import CustomJSONRenderer
from .services import *
import PyPDF2

class HealthCheckView(View):
	def get(self, request):
		return HttpResponse(status=200)

class UserApiView(APIView):
	renderer_classes = [CustomJSONRenderer]
	
	def get(self, request, *args, **kwargs):
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def post(self, request, *args, **kwargs):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QueryApiView(APIView):
	renderer_classes = [CustomJSONRenderer]
	parser_classes = [MultiPartParser, JSONParser]

	def get(self, request, *args, **kwargs):
		queries = Query.objects.all()
		serializer = QuerySerializer(queries, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		if request.FILES:
			query_serializer = QuerySerializer(data=process_request_data(request.data))
		else:
			query_serializer = QuerySerializer(data=request.data)

		if query_serializer.is_valid():
			query = query_serializer.save()
			results = QueryGPT.initiate_query(query)
			serializer = ResultSerializer(results, many=True)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def process_uploaded_file(file):
	pdf_reader = PyPDF2.PdfReader(file)
	combined_content = ""
	for page in pdf_reader.pages:
		page_content = page.extract_text()
		combined_content += page_content
	return combined_content

def process_request_data(data):
	data['tos'] = process_uploaded_file(data['file'])
	data['user'] = int(data.get('user'))
	del data['file']
	return data
