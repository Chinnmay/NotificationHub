"""
Common utilities for notification channels service

This package provides shared utilities for all channel consumers including
Kafka operations, configuration management, and message processing helpers.
"""

from .kafka_utils import get_topic_for_channel, deserialize_message, get_consumer_group

__all__ = ['get_topic_for_channel', 'deserialize_message', 'get_consumer_group']