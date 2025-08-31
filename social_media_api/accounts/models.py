from django.db import models

# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# accounts/models.py
class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )


    def __str__(self):
        return self.username

# Create your models here.
