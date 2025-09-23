from typing import Optional, Callable, Any
from functools import wraps
import graphene
import logging
import json



logger = logging.getLogger("django")


class ErrorType(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()

def format_graphql_error(field: Optional[str], message: str) -> ErrorType:
    return ErrorType(field=field, message=message)

def as_json_error(message: str, field: Optional[str] = None):
    payload = {"message": message}
    if field:
        payload = {"field": field, "message": message}
    return {"error": payload}

def log_error(exc: Exception, context: Optional[str] = None) -> None:
    if context:
        logger.exception("%s: %s", context, exc)
    else:
        logger.exception("Unhandled error: %s", exc)

def safe_signal_handler(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_error(e, context=f"Signal handler {func.__name__}")
            # swallow exception so signals don't break flow
            return None
    return wrapper

def graphql_format_error(error: Any):
    # error may be GraphQLError; return dict for GraphQLView.format_error
    try:
        message = str(error)
        # avoid leaking internal traceback in production; rely on logging
        return {"error": {"message": message}}
    except Exception as e:
        log_error(e, context="graphql_format_error")
        return {"error": {"message": "Internal server error"}}


# --- Channels Error Handler ---
async def send_ws_error(consumer, message, field=None):
    """Send a standardized error message over WebSocket."""
    await consumer.send(text_data=json.dumps(as_json_error(message, field)))