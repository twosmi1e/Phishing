from django.db import models

# Create your models here.
class Campaign(models.Model):
    name = models.CharField(max_length=20)