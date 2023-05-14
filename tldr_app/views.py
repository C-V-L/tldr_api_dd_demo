from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import UserSerializer, QuerySerializer, ResultSerializer
from .renderers import CustomJSONRenderer
from .services import *

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
    
    def get(self, request, *args, **kwargs):
      queries = Query.objects.all()
      serializer = QuerySerializer(queries, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
                
    def post(self, request, *args, **kwargs):
      query_serializer = QuerySerializer(data=request.data)

      if query_serializer.is_valid():
        validated_data = query_serializer.validated_data
        query = Query(user=User.objects.get(id=request.data['user']), areas_of_focus=request.data['areas_of_focus'], tos=request.data['tos'])
        query.save()
        result = Result(response=QueryGPT.initiate_query(query), query=query)
        result.save()
        serializer = ResultSerializer(result, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      else:
        return Response(query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
