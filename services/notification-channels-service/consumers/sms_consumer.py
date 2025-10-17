#!/usr/bin/env python3
"""
SMS notification consumer

This module implements a Kafka consumer for SMS notifications.
It processes messages from the SMS notification topic and handles
SMS delivery through a configurable SMS service provider.
"""

import asyncio
import signal
from typing import Dict, Any

from aiokafka import AIOKafkaConsumer
from common import get_topic_for_channel, deserialize_message, get_consumer_group
from common.config import KAFKA_BOOTSTRAP_SERVERS, SMS_DELAY_MS


async def send_sms(notification: Dict[str, Any]) -> bool:
    """Process and send SMS notification
    
    Args:
        notification: Notification data containing user info and message content
        
    Returns:
        True if SMS was sent successfully, False otherwise
    """
    try:
        user_id = notification.get('user_id', 'unknown')
        notification_id = notification.get('notification_id', 'unknown')
        data = notification.get('data', {})
        
        # Generate SMS content based on notification type
        message = f"Notification for {user_id}"
        if data.get('event_type') == 'payment.success':
            message = f"Payment of ${data.get('amount', 'N/A')} successful"
        
        # Generate dummy phone number
        phone = f"+1{user_id[-10:]}" if len(user_id) >= 10 else f"+1{user_id:0>10}"
        
        # Simulate SMS processing time
        await asyncio.sleep(SMS_DELAY_MS / 1000.0)
        
        print(f"📱 SMS SENT to {phone}")
        print(f"   Message: {message}")
        print(f"   Notification ID: {notification_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")
        return False


async def main():
    """Main SMS consumer event loop
    
    Sets up Kafka consumer connection and processes incoming SMS notifications
    from the SMS notification topic. Handles graceful shutdown on signals.
    """
    print("🚀 Starting SMS Notification Consumer...")
    
    # Create Kafka consumer
    consumer = AIOKafkaConsumer(
        get_topic_for_channel('sms'),
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=get_consumer_group('sms'),
        value_deserializer=deserialize_message,
        auto_offset_reset='earliest'
    )
    
    # Start consumer
    await consumer.start()
    print(f"✅ SMS Consumer started for topic: {get_topic_for_channel('sms')}")
    
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
                await send_sms(notification)
                
    except Exception as e:
        print(f"❌ SMS consumer error: {e}")
    finally:
        await consumer.stop()
        print("✅ SMS Consumer stopped")


if __name__ == "__main__":
    asyncio.run(main())