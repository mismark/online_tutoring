from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username