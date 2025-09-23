from channels.middleware.base import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Lazy import inside the function
        from rest_framework_simplejwt.tokens import UntypedToken
        from jwt import decode as jwt_decode, InvalidTokenError
        from django.conf import settings

        # Extract token from query params
        query_string = scope.get("query_string", b"").decode()
        token = None
        if query_string.startswith("token="):
            token = query_string.split("=", 1)[1]

        if token:
            try:
                # Validate token
                UntypedToken(token)

                # Decode token
                decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = decoded_data.get("user_id")

                # Get user
                user = await self.get_user(user_id)
                scope["user"] = user
            except InvalidTokenError:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
