from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post, Comment
from utils.cache import delete_cache



@receiver([post_save, post_delete], sender=Post)
def invalidate_feed_on_post_change(sender, **kwargs):
    delete_cache("feed_cache")

@receiver([post_save, post_delete], sender=Comment)
def invalidate_feed_on_comment_change(sender, **kwargs):
    delete_cache("feed_cache")
