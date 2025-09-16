from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Interaction
from utils.cache import delete_cache



@receiver([post_save, post_delete], sender=Interaction)
def invalidate_feed_on_interaction_change(sender, **kwargs):
    delete_cache("feed_cache")
