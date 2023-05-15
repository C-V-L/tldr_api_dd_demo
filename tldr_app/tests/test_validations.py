import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from tldr_app.models import User, Query, Result

class QueryModelTest(TestCase):
    def test_query(self):
        user = User.objects.create(name="Hady")
        query = Query.objects.create(user=user, areas_of_focus = ["a", "b"])
        with pytest.raises(ValidationError):
            query.full_clean()
    
    def test_query_second(self):
        user = User.objects.create(name = "Hady")
        query = Query.objects.create(user= user, tos = "hello")
        with pytest.raises(ValidationError):
            query.full_clean()

class UserModelTest(TestCase): 
    def test_user(self): 
        user_1 = User.objects.create()
        with pytest.raises(ValidationError):
            user_1.full_clean()

class ResultModelTest(TestCase):
    def test_result(self):
        user = User.objects.create(name = "Hady")
        query = Query.objects.create(user= user, areas_of_focus = ["a", "b"], tos = "Netflix Terms of Service")
        result = Result.objects.create(query = query)
        with pytest.raises(ValidationError):
            result.full_clean()