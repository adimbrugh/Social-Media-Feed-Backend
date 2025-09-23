from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.conf import settings
import jwt

# Delay imports until Django apps are ready
@database_sync_to_async
def _get_user_from_id(user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        return User.objects.get(pk=user_id)
    except Exception:
        return None


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

        # Extract token from query string
        qs = self.scope.get("query_string", b"").decode()
        if qs:
            for part in qs.split("&"):
                if part.startswith("token="):
                    token = part.split("=", 1)[1]
                    break

        # Extract token from headers if not in query
        if not token:
            headers = {k.decode(): v.decode() for k, v in self.scope.get("headers", [])}
            auth = headers.get("authorization") or headers.get("Authorization")
            if auth and auth.lower().startswith(("bearer ", "jwt ")):
                token = auth.split(" ", 1)[1]

        if token:
            try:
                # Import inside to avoid AppRegistryNotReady
                from rest_framework_simplejwt.tokens import UntypedToken
                from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

                # Validate token
                UntypedToken(token)

                # Decode payload
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"],
                    options={"verify_exp": True},
                )

                user = await _get_user_from_id(payload.get("user_id") or payload.get("sub"))
                if user:
                    self.scope["user"] = user

            except (InvalidToken, TokenError, jwt.PyJWTError):
                pass

        inner = self.inner(self.scope)
        return await inner(receive, send)
