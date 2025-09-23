from django.contrib.auth import get_user_model
from .types import UserType
import graphql_jwt
import graphene


UserModel = get_user_model()


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, username, email, password):
        if UserModel.objects.filter(username=username).exists():
            raise Exception("Username already taken")
        if UserModel.objects.filter(email=email).exists():
            raise Exception("Email already registered")

        user = UserModel.objects.create_user(username=username, email=email, password=password)
        return CreateUser(user=user)


class UpdateProfile(graphene.Mutation):
    class Arguments:
        bio = graphene.String()
        # profile_photo upload handling requires multipart handling; leave optional for now
    user = graphene.Field(UserType)

    def mutate(self, info, bio=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        if bio is not None:
            user.bio = bio
            user.save()
        return UpdateProfile(user=user)


class UserMutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_profile = UpdateProfile.Field()

    # graphql_jwt built-in fields
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
