from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import *
from .serializers import *
from .renderers import CustomJSONRenderer
from .services import *
import PyPDF2
import string

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

class CompareApiView(APIView):
	renderer_classes = [CustomJSONRenderer]
	parser_classes = [MultiPartParser, JSONParser]

	def post(self, request, *args, **kwargs):
		if 'user' not in request.data.keys():
			return Response({"user": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
		if request.FILES:
			processed_files = process_files(request)
			serialized_results = serialize_results(self, processed_files)
			return Response(serialized_results, status=status.HTTP_201_CREATED)
		elif 'tos1' in request.data.keys() and 'tos2' in request.data.keys():
			tos_array = tos_serializer(data=request.data)
			serialized_results = serialize_results(self, tos_array)
			return Response(serialized_results, status=status.HTTP_201_CREATED)
		else:
			return Response({"error": ["Need files or tos1/tos2"]}, status=status.HTTP_400_BAD_REQUEST)

def serialize_results(self, processed_files):
  result = QueryGPT.compare(self, processed_files)
  serialize_results = ComparisonSerializer(result, many=False)
  return serialize_results.data

def process_files(request):
		processed_file_1 = process_request_data(data=request.data, file_name='file1')
		tos_serializer_1 = TosSerializer(data=processed_file_1)
		if tos_serializer_1.is_valid():
			tos_1 = tos_serializer_1.save()
			
		processed_file_2 = process_request_data(data=request.data, file_name='file2')
		tos_serializer_2 = TosSerializer(data=processed_file_2)
		if tos_serializer_2.is_valid():
			tos_2 = tos_serializer_2.save()
		return [tos_1, tos_2]

def tos_serializer(data):
	data['tos'] = data['tos1']
	tos_serializer_1 = TosSerializer(data=data)
	if tos_serializer_1.is_valid():
		tos_1 = tos_serializer_1.save()
		data['tos'] = data['tos2']
	tos_serializer_2 = TosSerializer(data=data)
	if tos_serializer_2.is_valid():
		tos_2 = tos_serializer_2.save()
	return [tos_1, tos_2]

class QueryApiView(APIView):
	renderer_classes = [CustomJSONRenderer]
	parser_classes = [MultiPartParser, JSONParser]

	def get(self, request, *args, **kwargs):
		queries = Query.objects.all()
		serializer = QuerySerializer(queries, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		if 'user' not in request.data.keys():
			return Response({"user": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
		if request.FILES:
			processed_file = process_request_data(data=request.data, file_name='file')
			query_serializer = QuerySerializer(data=processed_file)
		else:
			query_serializer = QuerySerializer(data=request.data)
		if query_serializer.is_valid():
			query = query_serializer.save()
			results = QueryGPT.initiate_query(self, [query])
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
	combined_content = ''.join(char for char in combined_content if char in string.printable)
	return combined_content

def process_request_data(data, file_name):
	data['tos'] = process_uploaded_file(data[file_name])
	data['user'] = int(data.get('user'))
	del data[file_name]
	return data
