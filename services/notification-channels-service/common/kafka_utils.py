"""
Kafka utilities for notification channel consumers

This module provides utility functions for Kafka operations including
topic mapping, message deserialization, and consumer group management.
"""

import json
from typing import Dict, Any


def get_topic_for_channel(channel: str) -> str:
    """Get topic name for a channel"""
    from .config import KAFKA_TOPIC_EMAIL, KAFKA_TOPIC_SMS, KAFKA_TOPIC_WEBHOOK, KAFKA_TOPIC_SLACK
    
    topic_map = {
        'email': KAFKA_TOPIC_EMAIL,
        'sms': KAFKA_TOPIC_SMS,
        'webhook': KAFKA_TOPIC_WEBHOOK,
        'slack': KAFKA_TOPIC_SLACK,
    }
    return topic_map.get(channel, f"notifications.{channel}")


def deserialize_message(message_bytes: bytes) -> Dict[str, Any]:
    """Deserialize Kafka message"""
    try:
        return json.loads(message_bytes.decode('utf-8'))
    except Exception as e:
        print(f"❌ Failed to deserialize message: {e}")
        return {}


def get_consumer_group(channel: str) -> str:
    """Get consumer group for a channel"""
    from .config import KAFKA_CONSUMER_GROUP_PREFIX
    return f"{KAFKA_CONSUMER_GROUP_PREFIX}-{channel}"