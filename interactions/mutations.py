import graphene
from .types import InteractionType
from .models import Interaction
from posts.models import Post



class AddInteraction(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)
        type = graphene.String(required=True)  # "LIKE" or "SHARE"

    interaction = graphene.Field(InteractionType)

    def mutate(self, info, post_id, type):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        if type not in ["LIKE", "SHARE"]:
            raise Exception("Invalid interaction type")

        post = Post.objects.get(pk=post_id)

        interaction, created = Interaction.objects.get_or_create(user=user, post=post, type=type)
        return AddInteraction(interaction=interaction)


class RemoveInteraction(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)
        type = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, post_id, type):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        try:
            interaction = Interaction.objects.get(user=user, post_id=post_id, type=type)
            interaction.delete()
            return RemoveInteraction(success=True)
        except Interaction.DoesNotExist:
            return RemoveInteraction(success=False)


class InteractionMutations(graphene.ObjectType):
    add_interaction = AddInteraction.Field()
    remove_interaction = RemoveInteraction.Field()

