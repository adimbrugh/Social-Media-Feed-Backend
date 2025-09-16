import graphene
from .queries import PostQueries
from .mutations import PostMutations



class PostSchema(PostQueries, PostMutations, graphene.ObjectType):
    pass
