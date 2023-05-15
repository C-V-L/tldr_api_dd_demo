from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']

class QuerySerializer(serializers.ModelSerializer):
		areas_of_focus = serializers.ListField(required=True)
		tos = serializers.CharField(required=True)

		class Meta:
				model = Query
				fields = ['id', 'user', 'areas_of_focus', 'tos']

class ResultSerializer(serializers.ModelSerializer):
		class Meta:
				model = Result
				fields = ['id', 'response', 'query']