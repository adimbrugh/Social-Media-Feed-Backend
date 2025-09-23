from types import SimpleNamespace
import importlib
import pytest



def test_delete_cache_calls_cache(monkeypatch):
    ucache = importlib.import_module("utils.cache")
    called = {}
    class DummyCache:
        def delete(self, key):
            called["key"] = key
            return True
    monkeypatch.setattr(ucache, "cache", DummyCache())
    # call delete_cache (guarded against exceptions)
    ucache.delete_cache("my_key")
    assert called.get("key") == "my_key"