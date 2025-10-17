"""
Configuration management for notification core service

This module contains all configuration settings for the notification core service,
including Kafka connection parameters, API settings, logging configuration,
and event routing rules that determine which channels receive specific event types.
"""

import os
from typing import Dict, List

# Service settings
SERVICE_NAME = "Notification Core Service"
SERVICE_VERSION = "2.0.0"

# Kafka settings
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9094")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "notification-core")
KAFKA_AUTO_OFFSET_RESET = os.getenv("KAFKA_AUTO_OFFSET_RESET", "earliest")

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_RELOAD = os.getenv("API_RELOAD", "false").lower() == "true"

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Event routing rules
ROUTING_RULES: Dict[str, List[str]] = {
    'order.created': ['email', 'push', 'webhook', 'slack'],
    'order.cancelled': ['email', 'sms'],
    'payment.success': ['email', 'push'],
    'payment.failed': ['email', 'sms'],
    'user.registered': ['email'],
}

# Kafka topics (from shared constants)
SOURCE_TOPICS = [
    'order.events',
    'payment.events', 
    'user.events'
]

CHANNEL_TOPICS: Dict[str, str] = {
    'email': 'notifications.email',
    'sms': 'notifications.sms',
    'push': 'notifications.push',
    'webhook': 'notifications.webhook',
    'slack': 'notifications.slack',
}

# Notification settings
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5
PROCESSING_TIMEOUT_SECONDS = 30

# Settings object for easy access
class Settings:
    """Settings container"""
    
    # Service
    service_name = SERVICE_NAME
    service_version = SERVICE_VERSION
    
    # Kafka
    kafka_bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS
    kafka_consumer_group = KAFKA_CONSUMER_GROUP
    kafka_auto_offset_reset = KAFKA_AUTO_OFFSET_RESET
    
    # API
    api_host = API_HOST
    api_port = API_PORT
    api_reload = API_RELOAD
    
    # Logging
    log_level = LOG_LEVEL
    
    # Routing
    routing_rules = ROUTING_RULES
    source_topics = SOURCE_TOPICS
    channel_topics = CHANNEL_TOPICS
    
    # Notification
    max_retries = MAX_RETRIES
    retry_delay_seconds = RETRY_DELAY_SECONDS
    processing_timeout_seconds = PROCESSING_TIMEOUT_SECONDS

# Global settings instance
settings = Settings()
