from utils.cache import get_cache, set_cache
from .types import PostType
from .models import Post
import graphene



class PostQueries(graphene.ObjectType):
    feed = graphene.List(PostType, first=graphene.Int(), offset=graphene.Int())

    def resolve_feed(self, info, first=None, offset=None):
        cache_key = "feed_cache"
        feed_data = get_cache(cache_key)
        if feed_data:
            return feed_data  # return cached feed

        qs = Post.objects.select_related("author").prefetch_related("comments", "interactions").order_by("-created_at")
        if offset:
            qs = qs[offset:]
        if first:
            qs = qs[:first]

        # cache the feed (convert to list of dicts)
        feed_list = list(qs)
        set_cache(cache_key, [p.id for p in feed_list], timeout=60)  # cache IDs only

        return feed_list
