from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']

class QuerySerializer(serializers.ModelSerializer):
		areas_of_focus = serializers.ListField(child=serializers.CharField(max_length=200), required=True)
		tos = serializers.CharField(required=True)

		class Meta:
				model = Query
				fields = ['id', 'user', 'areas_of_focus', 'tos']

class ResultSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='response.title')
    impact = serializers.CharField(source='response.impact')
    actionable = serializers.CharField(source='response.actionable')
    ranking = serializers.IntegerField(source='response.ranking')

    class Meta:
        model = Result
        fields = ['title', 'impact', 'actionable', 'ranking']
        
class TosSerializer(serializers.ModelSerializer):
    tos = serializers.CharField(required=True)
    
    class Meta:
        model = Tos
        fields = ['tos']
        
class ComparisonSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='response.title')
    company_1 = serializers.CharField(source='response.company_1')
    company_2 = serializers.CharField(source='response.company_2')
    comparison = serializers.CharField(source='response.comparison')

    class Meta:
        model = Comparison
        fields = ['title', 'company_1', 'company_2', 'comparison']