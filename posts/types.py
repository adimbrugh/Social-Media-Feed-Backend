from graphene_django import DjangoObjectType
from .models import Post, Comment
import graphene



class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "content", "author", "post", "created_at")


class PostType(DjangoObjectType):
    likes_count = graphene.Int()
    shares_count = graphene.Int()
    comments_count = graphene.Int()

    class Meta:
        model = Post
        fields = ("id", "title", "content", "author", "created_at", "updated_at")

    def resolve_likes_count(self, info):
        return getattr(self, "likes_count", lambda: 0)()
    
    def resolve_shares_count(self, info):
        return getattr(self, "shares_count", lambda: 0)()

    def resolve_comments_count(self, info):
        return self.comments.count()

