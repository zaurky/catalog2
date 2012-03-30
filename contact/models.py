from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=255)

class Developer(models.Model):
    name = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
