from django.db import models

# Create your models here.
class User(models.Model):
    user_fname = models.CharField(max_length=30, null=False)