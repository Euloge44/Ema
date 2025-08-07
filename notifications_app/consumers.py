"""
Consumers WebSocket pour les notifications.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    Consumer WebSocket pour les notifications en temps réel.
    """
    
    async def connect(self):
        """Établir la connexion WebSocket."""
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'notifications_{self.user_id}'
        
        # Rejoindre le groupe de notifications
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Envoyer un message de confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connecté aux notifications'
        }))
    
    async def disconnect(self, close_code):
        """Fermer la connexion WebSocket."""
        # Quitter le groupe de notifications
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Recevoir un message du WebSocket."""
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'message')
        
        if message_type == 'mark_read':
            # Marquer une notification comme lue
            notification_id = text_data_json.get('notification_id')
            await self.mark_notification_read(notification_id)
    
    async def notification_message(self, event):
        """Envoyer une notification au WebSocket."""
        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': event['notification']
        }))
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Marquer une notification comme lue."""
        from .models import Notification
        try:
            notification = Notification.objects.get(id=notification_id, recipient_id=self.user_id)
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False