import graphene
from users.schema import UserSchema
from posts.schema import PostSchema
# import other app schemas as they become available, e.g. posts.schema.PostSchema



class Query(UserSchema, graphene.ObjectType):
    pass
class Mutation(UserSchema, graphene.ObjectType):
    pass


class Query(UserSchema, PostSchema, graphene.ObjectType):
    pass
class Mutation(UserSchema, PostSchema, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
