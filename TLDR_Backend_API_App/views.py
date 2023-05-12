from django.shortcuts import render

from rest_framework import viewsets
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all().order_by('name')
    serializer_class = MyModelSerializer
