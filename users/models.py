from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    # keep username field or switch to email-as-username later
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField(upload_to="profiles/", null=True, blank=True)
    bio = models.TextField(blank=True, default="")
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"  # change to "email" if you want email as login
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
