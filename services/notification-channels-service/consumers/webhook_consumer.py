#!/usr/bin/env python3
"""
Webhook notification consumer

This module implements a Kafka consumer for webhook notifications.
It processes messages from the webhook notification topic and handles
webhook delivery to configured endpoints.
"""

import asyncio
import signal
from typing import Dict, Any

from aiokafka import AIOKafkaConsumer
from common import get_topic_for_channel, deserialize_message, get_consumer_group
from common.config import KAFKA_BOOTSTRAP_SERVERS, WEBHOOK_DELAY_MS


async def send_webhook(notification: Dict[str, Any]) -> bool:
    """Process and send webhook notification
    
    Args:
        notification: Notification data containing user info and message content
        
    Returns:
        True if webhook was sent successfully, False otherwise
    """
    try:
        user_id = notification.get('user_id', 'unknown')
        notification_id = notification.get('notification_id', 'unknown')
        data = notification.get('data', {})
        
        # Prepare webhook payload
        payload = {
            'user_id': user_id,
            'notification_id': notification_id,
            'event_type': data.get('event_type', 'notification'),
            'timestamp': data.get('timestamp'),
            'data': data
        }
        
        # Generate dummy webhook URL
        webhook_url = f"https://api.example.com/webhooks/users/{user_id}/notifications"
        
        # Simulate webhook processing time
        await asyncio.sleep(WEBHOOK_DELAY_MS / 1000.0)
        
        print(f"🔗 WEBHOOK SENT to {webhook_url}")
        print(f"   Payload: {payload}")
        print(f"   Notification ID: {notification_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send webhook: {e}")
        return False


async def main():
    """Main webhook consumer event loop
    
    Sets up Kafka consumer connection and processes incoming webhook notifications
    from the webhook notification topic. Handles graceful shutdown on signals.
    """
    print("🚀 Starting Webhook Notification Consumer...")
    
    # Create Kafka consumer
    consumer = AIOKafkaConsumer(
        get_topic_for_channel('webhook'),
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=get_consumer_group('webhook'),
        value_deserializer=deserialize_message,
        auto_offset_reset='earliest'
    )
    
    # Start consumer
    await consumer.start()
    print(f"✅ WEBHOOK Consumer started for topic: {get_topic_for_channel('webhook')}")
    
    # Signal handling
    is_running = True
    
    def signal_handler(signum, frame):
        nonlocal is_running
        print(f"📡 Received signal {signum}, shutting down...")
        is_running = False
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Main processing loop
        async for message in consumer:
            if not is_running:
                break
                
            notification = message.value
            if notification:
                await send_webhook(notification)
                
    except Exception as e:
        print(f"❌ Webhook consumer error: {e}")
    finally:
        await consumer.stop()
        print("✅ Webhook Consumer stopped")


if __name__ == "__main__":
    asyncio.run(main())