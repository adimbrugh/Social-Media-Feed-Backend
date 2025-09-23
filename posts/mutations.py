from .types import PostType, CommentType
from .models import Post, Comment
import graphene



class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=False)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, content, title=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        post = Post.objects.create(author=user, title=title or "", content=content)
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, id, title=None, content=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Post not found")
        if post.author != user and not user.is_staff:
            raise Exception("You don't have permission to edit this post")

        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Post not found")
        if post.author != user and not user.is_staff:
            raise Exception("You don't have permission to delete this post")
        post.delete()
        return DeletePost(success=True)


class AddComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, post_id, content):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Exception("Post not found")
        comment = Comment.objects.create(post=post, author=user, content=content)
        return AddComment(comment=comment)


class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Authentication required")
        try:
            comment = Comment.objects.get(pk=id)
        except Comment.DoesNotExist:
            raise Exception("Comment not found")
        if comment.author != user and not user.is_staff:
            raise Exception("You don't have permission to delete this comment")
        comment.delete()
        return DeleteComment(success=True)


class PostMutations(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    add_comment = AddComment.Field()
    delete_comment = DeleteComment.Field()
