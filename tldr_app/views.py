from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import User, Query
from .serializers import UserSerializer, QuerySerializer
from .renderers import CustomJSONRenderer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    renderer_classes = [CustomJSONRenderer]
    
class QueryViewSet(viewsets.ModelViewSet):
    queryset = Query.objects.all().order_by('id')
    serializer_class = QuerySerializer
    renderer_classes = [CustomJSONRenderer]
