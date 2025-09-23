from .types import UserType
from .models import User
import graphene



class UserQueries(graphene.ObjectType):
    me = graphene.Field(UserType)
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            return None
        return user

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_user_by_id(self, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
