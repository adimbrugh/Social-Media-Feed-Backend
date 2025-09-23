from .queries import PostQueries
from .mutations import PostMutations
import graphene



class PostSchema(PostQueries, PostMutations, graphene.ObjectType):
    pass
