import graphene
from .queries import UserQueries
from .mutations import UserMutations



class UserSchema(UserQueries, UserMutations, graphene.ObjectType):
    pass
