from graphene_django import DjangoObjectType
from .models import User
import graphene



class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "profile_photo", "bio", "date_joined")
        
        
    