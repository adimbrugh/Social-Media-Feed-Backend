import graphene
from graphene_django import DjangoObjectType
from .models import Interaction



class InteractionType(DjangoObjectType):
    class Meta:
        model = Interaction
        fields = ("id", "user", "post", "type", "created_at")

