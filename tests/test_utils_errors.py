from utils.errors import format_graphql_error, as_json_error, ErrorType, safe_signal_handler
import pytest



def test_format_graphql_error():
    err = format_graphql_error("field_x", "oops")
    assert isinstance(err, ErrorType)
    assert err.field == "field_x"
    assert err.message == "oops"

def test_as_json_error():
    e = as_json_error("err msg", "f")
    assert e["error"]["field"] == "f"
    assert e["error"]["message"] == "err msg"

def test_safe_signal_handler_logs(monkeypatch):
    called = {}
    def fake_log_error(exc, context=None):
        called["ok"] = True
        called["ctx"] = context
    monkeypatch.setattr("utils.errors.log_error", fake_log_error)

    def will_raise(*a, **k):
        raise RuntimeError("boom")

    wrapped = safe_signal_handler(will_raise)
    # should not raise
    wrapped()
    assert called.get("ok") is True
    assert "Signal handler will_raise" in called.get("ctx", "")