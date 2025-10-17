"""
Event transformation engine for notification processing

This module provides the EventTransformer class which converts incoming
events into structured notifications and applies routing rules to determine
which notification channels should receive the message.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

def generate_id():
    return str(uuid.uuid4())

def get_current_timestamp():
    return datetime.utcnow()

def extract_user_id(data):
    return data.get('user_id') or data.get('userId')

def extract_event_type(data, topic=None):
    return data.get('event_type') or data.get('eventType')

from ..config.settings import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class EventTransformer:
    """Transforms events into notifications based on routing rules"""
    
    def __init__(self):
        self.routing_rules = settings.routing_rules
    
    def transform_event(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Transform a Kafka message into notifications
        
        Args:
            message: Kafka message with data and metadata
            
        Returns:
            List of notification dictionaries
        """
        try:
            data = message['data']
            topic = message['topic']
            
            # Extract event information
            event_type = extract_event_type(data, topic)
            user_id = extract_user_id(data)
            
            if not event_type or not user_id:
                logger.warning(f"⚠️ Invalid message - missing event_type or user_id: {data}")
                return []
            
            logger.info(f"📨 Transforming event: {event_type} for user {user_id}")
            
            # Check if event type is supported
            if event_type not in self.routing_rules:
                logger.warning(f"⚠️ Unsupported event type: {event_type}")
                return []
            
            # Get channels for this event type
            channels = self.routing_rules[event_type]
            
            if not channels:
                logger.info(f"ℹ️ No channels configured for event type: {event_type}")
                return []
            
            # Generate notifications for each channel
            notifications = []
            for channel in channels:
                notification = self._create_notification(
                    user_id, channel, event_type, data, topic
                )
                if notification:
                    notifications.append(notification)
            
            return notifications
            
        except Exception as e:
            logger.error(f"❌ Error transforming event: {e}")
            return []
    
    def _create_notification(
        self, 
        user_id: str, 
        channel: str, 
        event_type: str, 
        data: Dict[str, Any],
        source_topic: str
    ) -> Optional[Dict[str, Any]]:
        """
        Create a notification for a specific channel
        
        Args:
            user_id: User ID
            channel: Notification channel
            event_type: Event type
            data: Event data
            source_topic: Source Kafka topic
            
        Returns:
            Notification dictionary or None
        """
        try:
            # Enrich event data
            enriched_data = self._enrich_event_data(event_type, user_id, data)
            
            # Create notification
            notification = {
                "notification_id": generate_id(),
                "user_id": user_id,
                "channel": channel,
                "event_type": event_type,
                "data": enriched_data,
                "priority": self._get_notification_priority(event_type),
                "status": "pending",
                "created_at": get_current_timestamp().isoformat(),
                "source_topic": source_topic
            }
            
            return notification
            
        except Exception as e:
            logger.error(f"❌ Error creating notification for {channel}: {e}")
            return None
    
    def _enrich_event_data(self, event_type: str, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich event data with additional context
        
        Args:
            event_type: Event type
            user_id: User ID
            data: Original event data
            
        Returns:
            Enriched data dictionary
        """
        enriched_data = {
            **data,
            "event_type": event_type,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Add event-specific enrichments
        if event_type == "order.created":
            enriched_data.update({
                "order_summary": f"Order #{data.get('order_id', 'N/A')} has been created",
                "action_url": f"/orders/{data.get('order_id', '')}"
            })
        elif event_type == "order.cancelled":
            enriched_data.update({
                "order_summary": f"Order #{data.get('order_id', 'N/A')} has been cancelled",
                "action_url": f"/orders/{data.get('order_id', '')}"
            })
        elif event_type == "payment.success":
            enriched_data.update({
                "payment_summary": f"Payment of ${data.get('amount', 'N/A')} was successful",
                "receipt_url": f"/receipts/{data.get('payment_id', '')}"
            })
        elif event_type == "payment.failed":
            enriched_data.update({
                "payment_summary": f"Payment of ${data.get('amount', 'N/A')} failed",
                "retry_url": f"/payments/{data.get('payment_id', '')}/retry"
            })
        elif event_type == "user.registered":
            enriched_data.update({
                "welcome_message": f"Welcome {data.get('username', user_id)}!",
                "profile_url": f"/profile/{user_id}"
            })
        
        return enriched_data
    
    def _get_notification_priority(self, event_type: str) -> int:
        """
        Determine notification priority based on event type
        
        Args:
            event_type: Event type
            
        Returns:
            Priority level (1=low, 2=medium, 3=high)
        """
        high_priority_events = {"payment.failed", "order.cancelled"}
        medium_priority_events = {"order.created", "payment.success"}
        
        if event_type in high_priority_events:
            return 3  # High priority
        elif event_type in medium_priority_events:
            return 2  # Medium priority
        else:
            return 1  # Low priority
    
    def get_supported_event_types(self) -> List[str]:
        """Get list of supported event types"""
        return list(self.routing_rules.keys())
    
    def get_supported_channels(self) -> List[str]:
        """Get list of supported channels"""
        all_channels = set()
        for channels in self.routing_rules.values():
            all_channels.update(channels)
        return list(all_channels)
    
    def add_routing_rule(self, event_type: str, channels: List[str]) -> bool:
        """
        Add or update routing rule for an event type
        
        Args:
            event_type: Event type
            channels: List of channels
            
        Returns:
            True if successful
        """
        try:
            self.routing_rules[event_type] = channels
            logger.info(f"✅ Added routing rule: {event_type} → {channels}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to add routing rule: {e}")
            return False
