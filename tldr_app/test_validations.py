import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from tldr_app.models import User, Query

class QueryModelTest(TestCase):
    def test_query(self):
        user = User.objects.create(name = "Hady")
        with pytest.raises(ValidationError):
            Query.objects.create()
