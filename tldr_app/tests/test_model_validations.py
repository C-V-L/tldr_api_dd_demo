import pytest
from django.db import models
from django.test import TestCase
from django.core.exceptions import ValidationError
from tldr_app.models import *

class UserModelTest(TestCase): 
	def test_attributes(self):
		user = User.objects.create(name="Hady")
		assert user.name == "Hady"

	def test_validations(self): 
		user_1 = User.objects.create()
		with pytest.raises(ValidationError):
			user_1.full_clean()

class QueryModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create(name = "Hady")

	def test_attributes(self):
		query = Query.objects.create(
			user=self.user, 
			areas_of_focus = ["area", "box"], 
			tos="Netflix Terms of Service"
			)
		assert query.areas_of_focus == ["area", "box"]
		assert query.tos == "Netflix Terms of Service"
		assert query.user.name == "Hady"

	def test_validations(self):
		query = Query.objects.create(
			user=self.user, 
			areas_of_focus=["area", "box"]
			)
		with pytest.raises(ValidationError):
			query.full_clean()
    
	def test_validations_second(self):
		query = Query.objects.create(
			user= self.user, 
			tos="hello"
			)
		with pytest.raises(ValidationError):
			query.full_clean()

class ResultModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create(name="Hady")
		self.query = Query.objects.create(
			user=self.user, 
			areas_of_focus=["a", "b"], 
			tos="Netflix Terms of Service"
			)

	def test_attributes(self):
		result = Result.objects.create(
			response={"title": "focus", "impact": "message", "actionable": "message", "ranking": 1}, 
			query=self.query
			)
		assert result.response == {"title": "focus", "impact": "message", "actionable": "message", "ranking": 1}
		assert result.query is not None

	def test_validations(self):
		result = Result.objects.create(query=self.query)
		with pytest.raises(ValidationError):
			result.full_clean()
            
class TosModelTest(TestCase):
	def test_attributes(self):
		tos = Tos.objects.create(tos="Netflix Terms of Service")
		assert tos.tos == "Netflix Terms of Service"
        
	def test_validations(self):
		tos = Tos.objects.create()
		with pytest.raises(ValidationError):
			tos.full_clean()

class ComparisonModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create(name = "Hady")

	def test_attributes(self):
		comparison = Comparison.objects.create(
			user=self.user, 
			response={"title": "focus", "company_1": "Netflix", "company_2": "Hulu", "comparison": "message"}
			)
		assert comparison.user.name == 'Hady'
		assert comparison.response == {"title": "focus", "company_1": "Netflix", "company_2": "Hulu", "comparison": "message"}

	def test_validations(self):
		tos = Tos.objects.create()
		with pytest.raises(ValidationError):
			tos.full_clean()

class TosComparisonsModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create(name = "Hady")
		self.tos = Tos.objects.create(tos="Netflix Terms of Service")
		self.comparison = Comparison.objects.create(
			user=self.user,
			response={"title": "focus", "company_1": "Netflix", "company_2": "Hulu", "comparison": "message"}
		)

	def test_attributes(self):
		tos_comparisons = TosComparisons.objects.create(
			tos=self.tos,
			comparison=self.comparison
		)
		assert tos_comparisons.tos.tos == "Netflix Terms of Service"
		assert tos_comparisons.comparison == self.comparison

	# def test_validations(self):
	# 	tos_comparisons = TosComparisons.objects.create()
	# 	with pytest.raises(ValidationError):
	# 		tos_comparisons.full_clean()