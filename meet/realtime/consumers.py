from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
import json

User = get_user_model()


class MeetingConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for handling WebRTC signaling in meetings.
    """
    
    async def connect(self):
        self.meeting_id = self.scope['url_route']['kwargs']['meeting_id']
        self.room_group_name = f'meeting_{self.meeting_id}'
        self.user = self.scope['user']
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Notify others that a new user joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'user_id': self.user.id if self.user.is_authenticated else None,
                'username': self.user.username if self.user.is_authenticated else 'Anonymous'
            }
        )
    
    async def disconnect(self, close_code):
        # Notify others that user left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'user_id': self.user.id if self.user.is_authenticated else None,
                'username': self.user.username if self.user.is_authenticated else 'Anonymous'
            }
        )
        
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive_json(self, content):
        """
        Handle incoming WebSocket messages.
        Supports WebRTC signaling messages: offer, answer, ice-candidate
        """
        message_type = content.get('type')
        
        if message_type == 'offer':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_offer',
                    'offer': content.get('offer'),
                    'sender_id': self.user.id if self.user.is_authenticated else None
                }
            )
        
        elif message_type == 'answer':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_answer',
                    'answer': content.get('answer'),
                    'sender_id': self.user.id if self.user.is_authenticated else None
                }
            )
        
        elif message_type == 'ice-candidate':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ice_candidate',
                    'candidate': content.get('candidate'),
                    'sender_id': self.user.id if self.user.is_authenticated else None
                }
            )
    
    async def user_joined(self, event):
        """Send user joined notification"""
        await self.send_json({
            'type': 'user_joined',
            'user_id': event['user_id'],
            'username': event['username']
        })
    
    async def user_left(self, event):
        """Send user left notification"""
        await self.send_json({
            'type': 'user_left',
            'user_id': event['user_id'],
            'username': event['username']
        })
    
    async def webrtc_offer(self, event):
        """Send WebRTC offer to other peers"""
        await self.send_json({
            'type': 'offer',
            'offer': event['offer'],
            'sender_id': event['sender_id']
        })
    
    async def webrtc_answer(self, event):
        """Send WebRTC answer to other peers"""
        await self.send_json({
            'type': 'answer',
            'answer': event['answer'],
            'sender_id': event['sender_id']
        })
    
    async def ice_candidate(self, event):
        """Send ICE candidate to other peers"""
        await self.send_json({
            'type': 'ice-candidate',
            'candidate': event['candidate'],
            'sender_id': event['sender_id']
        })
