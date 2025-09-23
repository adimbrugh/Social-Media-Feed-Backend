from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from django.utils.module_loading import import_string
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from django.conf import settings
import jwt



User = get_user_model()


@database_sync_to_async
def _get_user_from_id(user_id):
    try:
        return User.objects.get(pk=user_id)
    except Exception:
        return None

if settings.configured:
    from rest_framework_simplejwt.tokens import UntypedToken
    
    
class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self.inner)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = dict(scope)
        self.inner = inner

    async def __call__(self, receive, send):
        self.scope["user"] = AnonymousUser()
        token = None

        qs = self.scope.get("query_string", b"").decode()
        if qs:
            for part in qs.split("&"):
                if part.startswith("token="):
                    token = part.split("=", 1)[1]
                    break

        if not token:
            headers = {k.decode(): v.decode() for k, v in self.scope.get("headers", [])}
            auth = headers.get("authorization") or headers.get("Authorization")
            if auth and auth.lower().startswith(("bearer ", "jwt ")):
                token = auth.split(" ", 1)[1]

        if token:
            try:
                # Validate token with SimpleJWT (raises on invalid/expired)
                UntypedToken(token)
                # decode to read user_id (uses same secret/alg as SimpleJWT)
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": True})
                user = await _get_user_from_id(payload.get("user_id") or payload.get("sub"))
                if user:
                    self.scope["user"] = user
            except (InvalidToken, TokenError, jwt.PyJWTError):
                pass

        inner = self.inner(self.scope)
        return await inner(receive, send)