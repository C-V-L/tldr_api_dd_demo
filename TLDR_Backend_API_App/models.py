from django.db import models

# Create your models here.
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=200)
    tos = models.TextField()
    
# from TLDR_Backend_API_App.models import MyModel
# MyModel.objects.all()[0].name
# MyModel.objects.all().filter(name="test1").values()