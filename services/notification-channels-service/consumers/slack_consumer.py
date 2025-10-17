#!/usr/bin/env python3
"""
Slack notification consumer

This module implements a Kafka consumer for Slack notifications.
It processes messages from the Slack notification topic and handles
Slack message delivery to configured channels or users.
"""

import asyncio
import signal
from typing import Dict, Any

from aiokafka import AIOKafkaConsumer
from common import get_topic_for_channel, deserialize_message, get_consumer_group
from common.config import KAFKA_BOOTSTRAP_SERVERS, SLACK_DELAY_MS


async def send_slack_message(notification: Dict[str, Any]) -> bool:
    """Process and send Slack notification
    
    Args:
        notification: Notification data containing user info and message content
        
    Returns:
        True if Slack message was sent successfully, False otherwise
    """
    try:
        user_id = notification.get('user_id', 'unknown')
        notification_id = notification.get('notification_id', 'unknown')
        data = notification.get('data', {})
        
        # Generate Slack message content
        event_type = data.get('event_type', 'notification')
        message = f"Notification for {user_id}"
        
        if event_type == 'order.created':
            message = f"🎉 Order #{data.get('order_id', 'N/A')} created for ${data.get('amount', 'N/A')}"
        elif event_type == 'payment.success':
            message = f"💳 Payment of ${data.get('amount', 'N/A')} successful"
        
        # Generate dummy channel name
        channel = f"#notifications-{user_id[:8]}"
        
        # Simulate Slack processing time
        await asyncio.sleep(SLACK_DELAY_MS / 1000.0)
        
        print(f"💬 SLACK MESSAGE SENT to {channel}")
        print(f"   Message: {message}")
        print(f"   Notification ID: {notification_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send Slack message: {e}")
        return False


async def main():
    """Main Slack consumer event loop
    
    Sets up Kafka consumer connection and processes incoming Slack notifications
    from the Slack notification topic. Handles graceful shutdown on signals.
    """
    print("🚀 Starting Slack Notification Consumer...")
    
    # Create Kafka consumer
    consumer = AIOKafkaConsumer(
        get_topic_for_channel('slack'),
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=get_consumer_group('slack'),
        value_deserializer=deserialize_message,
        auto_offset_reset='earliest'
    )
    
    # Start consumer
    await consumer.start()
    print(f"✅ SLACK Consumer started for topic: {get_topic_for_channel('slack')}")
    
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
                await send_slack_message(notification)
                
    except Exception as e:
        print(f"❌ Slack consumer error: {e}")
    finally:
        await consumer.stop()
        print("✅ Slack Consumer stopped")


if __name__ == "__main__":
    asyncio.run(main())