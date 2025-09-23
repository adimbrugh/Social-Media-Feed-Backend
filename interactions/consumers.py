from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get user from scope
        user = self.scope.get("user")
        if not user or user.is_anonymous:
            await self.close()
            return

        self.user = user
        self.group_name = f"user_{self.user.id}"

        # Add channel to group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove channel from group safely
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        # Send JSON payload
        message = event.get("message")
        if message:
            await self.send(text_data=json.dumps(message))
