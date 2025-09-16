import graphene
from users.schema import UserSchema
from posts.schema import PostSchema
from interactions.schema import InteractionSchema



class Query(UserSchema, graphene.ObjectType):
    pass
class Mutation(UserSchema, graphene.ObjectType):
    pass


class Query(UserSchema, PostSchema, graphene.ObjectType):
    pass
class Mutation(UserSchema, PostSchema, graphene.ObjectType):
    pass


class Query(UserSchema, PostSchema, InteractionSchema, graphene.ObjectType):
    pass
class Mutation(UserSchema, PostSchema, InteractionSchema, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
