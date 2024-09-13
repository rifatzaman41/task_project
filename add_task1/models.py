
from django.db import models
# Create your models here.
class TaskModel(models.Model):
     name=models.CharField(max_length=100)
     task=models.CharField(max_length=400)