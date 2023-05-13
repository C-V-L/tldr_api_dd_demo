from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)

class Query(models.Model):
    areas_of_focus = models.CharField(max_length=200)
    tos = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Result(models.Model):
		response = models.TextField()
		query = models.ForeignKey(Query, on_delete=models.CASCADE)    
# from TLDR_Backend_API_App.models import MyModel
# MyModel.objects.all()[0].name
# MyModel.objects.all().filter(name="test1").values()