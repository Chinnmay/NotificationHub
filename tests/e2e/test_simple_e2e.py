#!/usr/bin/env python3
"""
End-to-End Integration Test for Notification System

This test validates the complete notification processing pipeline:
1. Event ingestion through input topics
2. Message transformation and routing by core service
3. Notification delivery through channel services
4. Verification of end-to-end message flow

The test uses real Kafka connections and validates actual service behavior.
"""

import asyncio
import json
import time
import uuid
import sys
import os
from datetime import datetime, timezone
from typing import Dict, List
import logging

# Add services to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'services'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Test configuration
KAFKA_SERVER = "localhost:9094"
INPUT_TOPICS = {
    'order.events': ['order.created', 'order.cancelled'],
    'payment.events': ['payment.success', 'payment.failed'],
    'user.events': ['user.registered']
}
OUTPUT_TOPICS = ['notifications.email', 'notifications.sms', 'notifications.webhook', 'notifications.slack']

class SimpleE2ETest:
    """End-to-end integration test runner
    
    Manages Kafka connections, test data generation, and result verification
    for the complete notification system pipeline.
    """
    
    def __init__(self):
        self.sent_messages = []
        self.received_messages = {topic: [] for topic in OUTPUT_TOPICS}
        self.producer = None
        self.consumers = {}
    
    async def setup(self):
        """Initialize test environment and Kafka connections"""
        from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
        
        # Producer for sending events
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()
        logger.info("✅ Producer connected")
        
        # Consumers for monitoring notifications
        for topic in OUTPUT_TOPICS:
            consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=KAFKA_SERVER,
                group_id=f"e2e-test-{topic.split('.')[-1]}",
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest'
            )
            await consumer.start()
            self.consumers[topic] = consumer
            logger.info(f"✅ Consumer connected to {topic}")
    
    async def teardown(self):
        """Cleanup"""
        if self.producer:
            await self.producer.stop()
        for consumer in self.consumers.values():
            await consumer.stop()
        logger.info("✅ Cleanup complete")
    
    def create_test_events(self) -> List[Dict]:
        """Create simple test events"""
        events = []
        
        # Order events
        events.append({
            "event_id": str(uuid.uuid4()),
            "event_type": "order.created",
            "user_id": "test_user_001",
            "order_id": "order_12345",
            "amount": 99.99,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        events.append({
            "event_id": str(uuid.uuid4()),
            "event_type": "order.cancelled",
            "user_id": "test_user_002", 
            "order_id": "order_12346",
            "amount": 149.99,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        # Payment events
        events.append({
            "event_id": str(uuid.uuid4()),
            "event_type": "payment.success",
            "user_id": "test_user_003",
            "payment_id": "pay_78901",
            "amount": 99.99,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        events.append({
            "event_id": str(uuid.uuid4()),
            "event_type": "payment.failed",
            "user_id": "test_user_004",
            "payment_id": "pay_78902", 
            "amount": 149.99,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        # User events
        events.append({
            "event_id": str(uuid.uuid4()),
            "event_type": "user.registered",
            "user_id": "test_user_005",
            "email": "newuser@example.com",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        return events
    
    async def send_events(self, events: List[Dict]):
        """Send events to input topics"""
        logger.info(f"📤 Sending {len(events)} events...")
        
        for event in events:
            # Determine topic based on event type
            if event['event_type'].startswith('order'):
                topic = 'order.events'
            elif event['event_type'].startswith('payment'):
                topic = 'payment.events'
            elif event['event_type'].startswith('user'):
                topic = 'user.events'
            else:
                continue
            
            await self.producer.send(topic, event)
            self.sent_messages.append(event)
            logger.info(f"📤 Sent {event['event_type']} to {topic}")
            
            # Small delay between messages
            await asyncio.sleep(0.2)
        
        await self.producer.flush()
    
    async def monitor_notifications(self, timeout: int = 30):
        """Monitor output topics for notifications"""
        logger.info(f"👀 Monitoring notifications for {timeout} seconds...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            for topic, consumer in self.consumers.items():
                try:
                    # Get message with short timeout
                    message = await asyncio.wait_for(consumer.__anext__(), timeout=0.1)
                    notification = message.value
                    self.received_messages[topic].append(notification)
                    logger.info(f"📥 Received {notification.get('event_type', 'unknown')} from {topic}")
                except asyncio.TimeoutError:
                    continue
                except StopAsyncIteration:
                    continue
            
            # Check if we got enough messages
            total_received = sum(len(msgs) for msgs in self.received_messages.values())
            if total_received >= 5:  # We expect at least 5 notifications
                logger.info("✅ Received sufficient notifications")
                break
            
            await asyncio.sleep(0.5)
    
    def verify_results(self):
        """Verify test results"""
        logger.info("🔍 Verifying results...")
        
        total_sent = len(self.sent_messages)
        total_received = sum(len(msgs) for msgs in self.received_messages.values())
        
        logger.info(f"📊 Results:")
        logger.info(f"  📤 Events sent: {total_sent}")
        logger.info(f"  📥 Notifications received: {total_received}")
        
        for topic, messages in self.received_messages.items():
            if messages:
                logger.info(f"    - {topic}: {len(messages)} messages")
        
        # Simple verification - we should have received some notifications
        if total_received == 0:
            raise AssertionError("❌ No notifications received!")
        
        logger.info("✅ Test verification passed!")
    
    async def run_test(self):
        """Run the complete E2E test"""
        logger.info("🚀 Starting Simple E2E Test...")
        
        try:
            # Setup
            await self.setup()
            
            # Wait for consumers to be ready
            await asyncio.sleep(3)
            
            # Create and send events
            events = self.create_test_events()
            await self.send_events(events)
            
            # Monitor for notifications
            await self.monitor_notifications()
            
            # Verify results
            self.verify_results()
            
            logger.info("🎉 E2E Test completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ E2E Test failed: {e}")
            raise
        finally:
            await self.teardown()

# Test function
async def test_simple_e2e():
    """Simple E2E test"""
    test = SimpleE2ETest()
    await test.run_test()

if __name__ == "__main__":
    print("🧪 Simple E2E Test for Notification System")
    print(f"📡 Kafka: {KAFKA_SERVER}")
    print(f"📥 Input Topics: {list(INPUT_TOPICS.keys())}")
    print(f"📤 Output Topics: {OUTPUT_TOPICS}")
    print()
    
    try:
        asyncio.run(test_simple_e2e())
        print("\n🎉 Simple E2E Test passed!")
    except Exception as e:
        print(f"\n❌ Simple E2E Test failed: {e}")
        exit(1)