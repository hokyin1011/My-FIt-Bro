from django.db import models

# Create your models here.
class user(models.Model):
    username = models.CharField
    password = models.CharField(max_length=20)