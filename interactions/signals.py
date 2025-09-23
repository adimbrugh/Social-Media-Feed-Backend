from django.db.models.signals import post_save, post_delete
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from .models import Interaction
import utils.cache as cache  



channel_layer = get_channel_layer()


@receiver([post_save, post_delete], sender=Interaction)
def invalidate_feed_on_interaction_change(sender, **kwargs):
    cache.delete_cache("feed_cache")

@receiver(post_save, sender=Interaction)
def notify_user_on_interaction(sender, instance, created, **kwargs):
    if created:
        post_author = instance.post.author
        message = {
            "type": "send_notification",
            "message": {
                "text": f"{instance.user.username} {instance.type}d your post",
                "post_id": instance.post.id,
                "interaction_type": instance.type
            }
        }
        async_to_sync(channel_layer.group_send)(f"user_{post_author.id}", message)
