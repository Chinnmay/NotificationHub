"""
Event consumer for Kafka message processing

This module provides the EventConsumer class which handles consuming
events from Kafka topics and processing them through the notification
transformation pipeline.
"""

from typing import AsyncGenerator, Dict, Any
import asyncio

from ..config.settings import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class EventConsumer:
    """Handles Kafka consumer operations for events"""
    
    def __init__(self):
        self.consumer = None
        self.is_started = False
    
    async def start(self):
        """Start the Kafka consumer"""
        if self.is_started:
            logger.warning("⚠️ Consumer already started")
            return
        
        try:
            from aiokafka import AIOKafkaConsumer
            
            self.consumer = AIOKafkaConsumer(
                *settings.source_topics,
                bootstrap_servers=settings.kafka_bootstrap_servers,
                group_id=settings.kafka_consumer_group,
                value_deserializer=lambda m: self._deserialize_message(m),
                auto_offset_reset=settings.kafka_auto_offset_reset
            )
            await self.consumer.start()
            self.is_started = True
            logger.info(f"✅ Kafka Consumer started for topics: {settings.source_topics}")
            
        except Exception as e:
            logger.error(f"❌ Failed to start Kafka Consumer: {e}")
            raise
    
    async def stop(self):
        """Stop the Kafka consumer"""
        if self.consumer and self.is_started:
            await self.consumer.stop()
            self.is_started = False
            logger.info("🛑 Kafka Consumer stopped")
    
    def _deserialize_message(self, message_bytes: bytes) -> Dict[str, Any]:
        """Deserialize Kafka message"""
        try:
            import json
            return json.loads(message_bytes.decode('utf-8'))
        except Exception as e:
            logger.error(f"❌ Failed to deserialize message: {e}")
            return {}
    
    async def consume_messages(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Consume messages from Kafka
        
        Yields:
            Dictionary containing message data and metadata
        """
        if not self.is_started:
            raise RuntimeError("Consumer not started. Call start() first.")
        
        try:
            async for message in self.consumer:
                yield {
                    'topic': message.topic,
                    'partition': message.partition,
                    'offset': message.offset,
                    'timestamp': message.timestamp,
                    'data': message.value,
                    'headers': message.headers
                }
        except Exception as e:
            logger.error(f"❌ Error consuming messages: {e}")
            raise
    
    async def process_events_loop(self, transformer, producer):
        """
        Main event processing loop
        
        Args:
            transformer: EventTransformer instance
            producer: NotificationProducer instance
        """
        logger.info("📥 Starting event processing loop...")
        
        try:
            async for message in self.consume_messages():
                await self._process_single_message(message, transformer, producer)
        except Exception as e:
            logger.error(f"❌ Error in event processing loop: {e}")
        finally:
            logger.info("🛑 Event processing loop stopped")
    
    async def _process_single_message(self, message: Dict[str, Any], transformer, producer):
        """
        Process a single Kafka message
        
        Args:
            message: Message data from Kafka
            transformer: EventTransformer instance
            producer: NotificationProducer instance
        """
        try:
            # Transform event into notifications
            notifications = transformer.transform_event(message)
            
            if not notifications:
                logger.debug(f"ℹ️ No notifications generated for message from {message['topic']}")
                return
            
            # Send each notification
            for notification in notifications:
                success = await producer.send_notification(
                    notification['channel'], 
                    notification
                )
                
                if success:
                    logger.info(f"📤 Sent {notification['channel']} notification to user {notification['user_id']}")
                else:
                    logger.error(f"❌ Failed to send {notification['channel']} notification")
                    
        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")
    
    def is_ready(self) -> bool:
        """Check if consumer is ready"""
        return self.is_started and self.consumer is not None
