from django.db import models
from django.contrib.auth import get_user_model

class Mango(models.Model):
  country = models.CharField(max_length=60)
  state = models.CharField(max_length=30)
  city = models.CharField(max_length=100)
  description = models.TextField()
