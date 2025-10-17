#!/usr/bin/env python3
"""
Notification Core Service - Main Application Entry Point

This service serves as the central hub for notification processing, consuming
events from various Kafka topics and transforming them into structured
notifications for delivery through multiple channels including email, SMS,
webhooks, and Slack integrations.
"""

import asyncio
import signal
from typing import Optional

from .config.settings import settings
from .utils.logger import setup_logger, get_logger
from .core import EventConsumer, NotificationProducer, EventTransformer

# Setup logging
logger = setup_logger()

# Global instances
consumer: Optional[EventConsumer] = None
producer: Optional[NotificationProducer] = None
transformer: Optional[EventTransformer] = None


async def start_service():
    """Initialize and start all core service components
    
    Sets up the event consumer, notification producer, and event transformer
    components to begin processing the notification pipeline.
    """
    global consumer, producer, transformer
    
    logger.info(f"🚀 Starting {settings.service_name} v{settings.service_version}")
    
    try:
        # Initialize components
        consumer = EventConsumer()
        producer = NotificationProducer()
        transformer = EventTransformer()
        
        # Start components
        logger.info("📡 Starting Kafka components...")
        await producer.start()
        await consumer.start()
        
        logger.info("✅ All components started successfully")
        
        # Start the main processing loop
        logger.info("🔄 Starting event processing loop...")
        await consumer.process_events_loop(transformer, producer)
        
    except Exception as e:
        logger.error(f"❌ Failed to start service: {e}")
        await stop_service()
        raise


async def stop_service():
    """Stop all service components"""
    global consumer, producer
    
    logger.info("🛑 Stopping service...")
    
    try:
        if consumer:
            await consumer.stop()
        if producer:
            await producer.stop()
        
        logger.info("✅ Service stopped successfully")
        
    except Exception as e:
        logger.error(f"❌ Error stopping service: {e}")


def setup_signal_handlers():
    """Setup signal handlers for graceful shutdown"""
    
    def signal_handler(signum, frame):
        logger.info(f"📡 Received signal {signum}, initiating graceful shutdown...")
        asyncio.create_task(stop_service())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


async def main():
    """Main entry point"""
    try:
        # Setup signal handlers
        setup_signal_handlers()
        
        # Start the service
        await start_service()
        
    except KeyboardInterrupt:
        logger.info("📡 Keyboard interrupt received")
    except Exception as e:
        logger.error(f"❌ Service failed: {e}")
        raise
    finally:
        await stop_service()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("📡 Service interrupted by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        exit(1)
