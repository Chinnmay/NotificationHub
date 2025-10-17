"""
Notification producer for Kafka message publishing

This module provides the NotificationProducer class which handles publishing
transformed notifications to appropriate Kafka topics for channel-specific
consumers to process.
"""

import json
from typing import Dict, Any, Optional

from ..config.settings import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class NotificationProducer:
    """Handles Kafka producer operations for notifications"""
    
    def __init__(self):
        self.producer = None
        self.is_started = False
    
    async def start(self):
        """Start the Kafka producer"""
        if self.is_started:
            logger.warning("⚠️ Producer already started")
            return
        
        try:
            from aiokafka import AIOKafkaProducer
            
            self.producer = AIOKafkaProducer(
                bootstrap_servers=settings.kafka_bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            await self.producer.start()
            self.is_started = True
            logger.info("✅ Kafka Producer started")
            
        except Exception as e:
            logger.error(f"❌ Failed to start Kafka Producer: {e}")
            raise
    
    async def stop(self):
        """Stop the Kafka producer"""
        if self.producer and self.is_started:
            await self.producer.stop()
            self.is_started = False
            logger.info("🛑 Kafka Producer stopped")
    
    async def send_message(self, topic: str, message: Dict[str, Any]) -> bool:
        """
        Send a message to a Kafka topic
        
        Args:
            topic: Kafka topic name
            message: Message data to send
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.is_started:
                await self.start()
            
            await self.producer.send_and_wait(topic, message)
            logger.debug(f"📤 Message sent to topic {topic}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send message to {topic}: {e}")
            return False
    
    async def send_notification(self, channel: str, notification_data: Dict[str, Any]) -> bool:
        """
        Send a notification to the appropriate channel topic
        
        Args:
            channel: Notification channel (email, sms, push)
            notification_data: Notification data
            
        Returns:
            True if successful, False otherwise
        """
        topic = settings.channel_topics.get(channel)
        if not topic:
            logger.warning(f"⚠️ Unknown channel: {channel}")
            return False
        
        return await self.send_message(topic, notification_data)
    
    def is_ready(self) -> bool:
        """Check if producer is ready"""
        return self.is_started and self.producer is not None
