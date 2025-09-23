from .types import InteractionType
from .models import Interaction
import graphene



class InteractionQueries(graphene.ObjectType):
    all_interactions = graphene.List(InteractionType)
    interactions_by_post = graphene.List(InteractionType, post_id=graphene.Int(required=True))
    interactions_by_user = graphene.List(InteractionType, user_id=graphene.Int(required=True))

    def resolve_all_interactions(self, info):
        return Interaction.objects.select_related("user", "post").all()

    def resolve_interactions_by_post(self, info, post_id):
        return Interaction.objects.filter(post_id=post_id).select_related("user")

    def resolve_interactions_by_user(self, info, user_id):
        return Interaction.objects.filter(user_id=user_id).select_related("post")

