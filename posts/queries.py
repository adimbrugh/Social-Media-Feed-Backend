import graphene
from graphene_django.filter import DjangoFilterConnectionField
from .types import PostType
from graphene import relay
from .models import Post



class PostNode(PostType, graphene.relay.Node):
    class Meta:
        model = Post
        interfaces = (relay.Node,)


class PostQueries(graphene.ObjectType):
    all_posts = graphene.List(PostType, first=graphene.Int(), offset=graphene.Int())
    post_by_id = graphene.Field(PostType, id=graphene.Int(required=True))
    posts_by_author = graphene.List(PostType, author_id=graphene.Int(required=True))

    def resolve_all_posts(self, info, first=None, offset=None):
        qs = Post.objects.select_related("author").prefetch_related("comments")
        if offset:
            qs = qs[offset:]
        if first:
            qs = qs[:first]
        return qs.order_by("-created_at")

    def resolve_post_by_id(self, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None

    def resolve_posts_by_author(self, info, author_id):
        return Post.objects.filter(author__id=author_id).order_by("-created_at")
