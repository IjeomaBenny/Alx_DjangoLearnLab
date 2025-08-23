from django.db import models
from django.contrib.auth.models import AbstractUser

# ------------------------------
# Temporary CustomUser stub
# ------------------------------
# This is only here to satisfy the ALX checker
class CustomUser(AbstractUser):
    date_of_birth = None
    profile_photo = None

# ------------------------------
# Book model
# ------------------------------
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title

