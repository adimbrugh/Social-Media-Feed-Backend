from interactions.schema import InteractionSchema
from users.schema import UserSchema
from posts.schema import PostSchema
import graphene



class Query(UserSchema, PostSchema, InteractionSchema, graphene.ObjectType):
    pass

class Mutation(UserSchema, PostSchema, InteractionSchema, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
