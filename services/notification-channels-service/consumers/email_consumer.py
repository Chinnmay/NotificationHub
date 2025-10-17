#!/usr/bin/env python3
"""
Email notification consumer

This module implements a Kafka consumer for email notifications.
It processes messages from the email notification topic and handles
email delivery through a configurable email service provider.
"""

import asyncio
import signal
from typing import Dict, Any

from aiokafka import AIOKafkaConsumer
from common import get_topic_for_channel, deserialize_message, get_consumer_group
from common.config import KAFKA_BOOTSTRAP_SERVERS, EMAIL_DELAY_MS


async def send_email(notification: Dict[str, Any]) -> bool:
    """Process and send email notification
    
    Args:
        notification: Notification data containing user info and message content
        
    Returns:
        True if email was sent successfully, False otherwise
    """
    try:
        user_id = notification.get('user_id', 'unknown')
        notification_id = notification.get('notification_id', 'unknown')
        data = notification.get('data', {})
        
        # Generate email content based on notification type
        subject = f"Notification for {user_id}"
        if data.get('event_type') == 'order.created':
            subject = f"Order #{data.get('order_id', 'N/A')} Confirmed"
        
        # Simulate email processing time
        await asyncio.sleep(EMAIL_DELAY_MS / 1000.0)
        
        print(f"📧 EMAIL SENT to {user_id}@example.com")
        print(f"   Subject: {subject}")
        print(f"   Notification ID: {notification_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


async def main():
    """Main email consumer event loop
    
    Sets up Kafka consumer connection and processes incoming email notifications
    from the email notification topic. Handles graceful shutdown on signals.
    """
    print("🚀 Starting Email Notification Consumer...")
    
    # Create Kafka consumer
    consumer = AIOKafkaConsumer(
        get_topic_for_channel('email'),
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=get_consumer_group('email'),
        value_deserializer=deserialize_message,
        auto_offset_reset='earliest'
    )
    
    # Start consumer
    await consumer.start()
    print(f"✅ EMAIL Consumer started for topic: {get_topic_for_channel('email')}")
    
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
                await send_email(notification)
                
    except Exception as e:
        print(f"❌ Email consumer error: {e}")
    finally:
        await consumer.stop()
        print("✅ Email Consumer stopped")


if __name__ == "__main__":
    asyncio.run(main())