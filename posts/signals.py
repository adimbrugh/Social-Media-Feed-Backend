from django.db.models.signals import post_save, post_delete
from utils.errors import safe_signal_handler
from django.dispatch import receiver
from .models import Post, Comment
import utils.cache as cache  



@safe_signal_handler
@receiver([post_save, post_delete], sender=Post)
def invalidate_feed_on_post_change(sender, **kwargs):
    cache.delete_cache("feed_cache")

@safe_signal_handler
@receiver([post_save, post_delete], sender=Comment)
def invalidate_feed_on_comment_change(sender, **kwargs):
    cache.delete_cache("feed_cache")
