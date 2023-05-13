from rest_framework import serializers
from .models import User, Query

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']

class QuerySerializer(serializers.ModelSerializer):
		class Meta:
				model = Query
				fields = ['id', 'user', 'areas_of_focus', 'tos']