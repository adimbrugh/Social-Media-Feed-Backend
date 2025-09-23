from django.contrib.auth import get_user_model
from posts.models import Post
import importlib
import pytest



User = get_user_model()


@pytest.mark.django_db
def test_post_save_triggers_cache_invalidation(monkeypatch):
    # import signals module so handlers are connected
    signals_mod = importlib.import_module("posts.signals")

    called = {}
    def fake_delete_cache(k):
        called["key"] = k

    # Patch the function in the place the signal uses it.
    # Prefer patching posts.signals.cache.delete_cache if available, else utils.cache.delete_cache.
    if hasattr(signals_mod, "cache") and hasattr(signals_mod.cache, "delete_cache"):
        monkeypatch.setattr(signals_mod.cache, "delete_cache", fake_delete_cache, raising=True)
    else:
        ucache = importlib.import_module("utils.cache")
        monkeypatch.setattr(ucache, "delete_cache", fake_delete_cache, raising=True)

    try:
        user = User.objects.create_user(username="tuser", password="pass")
    except TypeError:
        user = User.objects.create(username="tuser")

    Post.objects.create(author=user, content="hello")
    assert called.get("key") is not None