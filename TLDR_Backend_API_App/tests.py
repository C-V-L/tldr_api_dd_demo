from django.test import TestCase
from TLDR_Backend_API_App.models import MyModel

class MyModelTestCase(TestCase):
    def setUp(self):
        MyModel.objects.create(name="test1")
        MyModel.objects.create(name="test2")

    def test_MyModel(self):
        """MyModel are correctly identified"""
        test1 = MyModel.objects.get(name="test1")
        test2 = MyModel.objects.get(name="test2")

        self.assertEqual(test1.name, "test1")
        self.assertEqual(test2.name, "test2")