import graphene
from graphene_django import DjangoObjectType
from .models import User



class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "profile_photo", "bio", "date_joined")
        # You can add more fields as needed 
        # or use exclude = ("password",) to exclude sensitive fields
        