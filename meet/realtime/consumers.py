from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
import json
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class MeetingConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for handling WebRTC signaling in meetings.
    Supports: offer, answer, ice-candidate, join-call, leave-call messages
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.meeting_id = self.scope['url_route']['kwargs']['meeting_id']
        self.room_group_name = f'meeting_{self.meeting_id}'
        self.user = self.scope['user']
        
        # Check if user is authenticated
        if not self.user.is_authenticated:
            logger.warning(f"Unauthenticated user attempted to join meeting {self.meeting_id}")
            await self.close(code=4001)
            return
        
        # Verify user has access to this meeting
        has_access = await self.check_meeting_access()
        if not has_access:
            logger.warning(f"User {self.user.id} attempted to access unauthorized meeting {self.meeting_id}")
            await self.close(code=4003)
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"User {self.user.id} connected to meeting {self.meeting_id}")
        
        # Notify others that a new user joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'user_id': self.user.id,
                'username': self.user.username,
                'email': self.user.email
            }
        )
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if self.user.is_authenticated:
            # Notify others that user left
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_left',
                    'user_id': self.user.id,
                    'username': self.user.username
                }
            )
            
            logger.info(f"User {self.user.id} disconnected from meeting {self.meeting_id}")
        
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive_json(self, content):
        """
        Handle incoming WebSocket messages.
        Supports WebRTC signaling messages: offer, answer, ice-candidate, join-call, leave-call
        """
        try:
            message_type = content.get('type')
            
            if not message_type:
                await self.send_json({
                    'type': 'error',
                    'message': 'Message type is required'
                })
                return
            
            if message_type == 'offer':
                await self.handle_offer(content)
            elif message_type == 'answer':
                await self.handle_answer(content)
            elif message_type == 'ice-candidate':
                await self.handle_ice_candidate(content)
            elif message_type == 'join-call':
                await self.handle_join_call(content)
            elif message_type == 'leave-call':
                await self.handle_leave_call(content)
            else:
                await self.send_json({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}'
                })
                
        except Exception as e:
            logger.error(f"Error handling message in meeting {self.meeting_id}: {str(e)}")
            await self.send_json({
                'type': 'error',
                'message': 'Internal server error processing your message'
            })
    
    async def handle_offer(self, content):
        """Handle WebRTC offer"""
        offer = content.get('offer')
        target_id = content.get('target_id')  # Specific peer to send to
        
        if not offer:
            await self.send_json({
                'type': 'error',
                'message': 'Offer data is required'
            })
            return
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'webrtc_offer',
                'offer': offer,
                'sender_id': self.user.id,
                'sender_username': self.user.username,
                'target_id': target_id
            }
        )
    
    async def handle_answer(self, content):
        """Handle WebRTC answer"""
        answer = content.get('answer')
        target_id = content.get('target_id')
        
        if not answer:
            await self.send_json({
                'type': 'error',
                'message': 'Answer data is required'
            })
            return
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'webrtc_answer',
                'answer': answer,
                'sender_id': self.user.id,
                'sender_username': self.user.username,
                'target_id': target_id
            }
        )
    
    async def handle_ice_candidate(self, content):
        """Handle ICE candidate"""
        candidate = content.get('candidate')
        target_id = content.get('target_id')
        
        if not candidate:
            await self.send_json({
                'type': 'error',
                'message': 'ICE candidate data is required'
            })
            return
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'ice_candidate',
                'candidate': candidate,
                'sender_id': self.user.id,
                'target_id': target_id
            }
        )
    
    async def handle_join_call(self, content):
        """Handle user joining call"""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_joined',
                'user_id': self.user.id,
                'username': self.user.username,
                'timestamp': content.get('timestamp')
            }
        )
    
    async def handle_leave_call(self, content):
        """Handle user leaving call"""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'call_left',
                'user_id': self.user.id,
                'username': self.user.username,
                'timestamp': content.get('timestamp')
            }
        )
    
    @database_sync_to_async
    def check_meeting_access(self):
        """Check if user has access to the meeting"""
        from meetings.models import Meeting, MeetingParticipant
        
        try:
            meeting = Meeting.objects.get(id=self.meeting_id)
            # Check if user is host or participant
            if meeting.host == self.user:
                return True
            return MeetingParticipant.objects.filter(
                meeting=meeting,
                user=self.user
            ).exists()
        except Meeting.DoesNotExist:
            return False
    
    async def user_joined(self, event):
        """Send user joined notification"""
        await self.send_json({
            'type': 'user_joined',
            'user_id': event['user_id'],
            'username': event['username'],
            'email': event.get('email', '')
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
        # Only send to target peer if specified, otherwise broadcast
        if event.get('target_id') and event['target_id'] != self.user.id:
            return
        
        await self.send_json({
            'type': 'offer',
            'offer': event['offer'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username']
        })
    
    async def webrtc_answer(self, event):
        """Send WebRTC answer to other peers"""
        if event.get('target_id') and event['target_id'] != self.user.id:
            return
        
        await self.send_json({
            'type': 'answer',
            'answer': event['answer'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username']
        })
    
    async def ice_candidate(self, event):
        """Send ICE candidate to other peers"""
        if event.get('target_id') and event['target_id'] != self.user.id:
            return
        
        await self.send_json({
            'type': 'ice-candidate',
            'candidate': event['candidate'],
            'sender_id': event['sender_id']
        })
    
    async def call_joined(self, event):
        """Send call joined notification"""
        await self.send_json({
            'type': 'call-joined',
            'user_id': event['user_id'],
            'username': event['username'],
            'timestamp': event.get('timestamp')
        })
    
    async def call_left(self, event):
        """Send call left notification"""
        await self.send_json({
            'type': 'call-left',
            'user_id': event['user_id'],
            'username': event['username'],
            'timestamp': event.get('timestamp')
        })

