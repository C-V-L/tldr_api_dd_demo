from django.core import management
from django.test import TestCase
from tldr_app.models import *

def test_clear_data(db): 
  random_user = User.objects.create(name="Hady")
  Query.objects.create(tos="Sample TOS.", user=random_user, areas_of_focus= ["mandatory binding arbitration", "focus"])
  assert User.objects.count() == 1
  assert Query.objects.count() == 1
  management.call_command('clear_data')
  assert User.objects.count() == 0
  assert Query.objects.count() == 0
