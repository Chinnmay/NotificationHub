"""
Configuration management for notification channels service

This module contains environment-based configuration settings for the
notification channels service, including Kafka connection details,
topic names, and processing delays.
"""

import os

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9094')
KAFKA_CONSUMER_GROUP_PREFIX = os.getenv('KAFKA_CONSUMER_GROUP_PREFIX', 'notification')

# Topic Configuration
KAFKA_TOPIC_EMAIL = os.getenv('KAFKA_TOPIC_EMAIL', 'notifications.email')
KAFKA_TOPIC_SMS = os.getenv('KAFKA_TOPIC_SMS', 'notifications.sms')
KAFKA_TOPIC_WEBHOOK = os.getenv('KAFKA_TOPIC_WEBHOOK', 'notifications.webhook')
KAFKA_TOPIC_SLACK = os.getenv('KAFKA_TOPIC_SLACK', 'notifications.slack')

# Channel Delays (in milliseconds)
EMAIL_DELAY_MS = int(os.getenv('EMAIL_DELAY_MS', '100'))
SMS_DELAY_MS = int(os.getenv('SMS_DELAY_MS', '150'))
WEBHOOK_DELAY_MS = int(os.getenv('WEBHOOK_DELAY_MS', '200'))
SLACK_DELAY_MS = int(os.getenv('SLACK_DELAY_MS', '120'))

# Service Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
SERVICE_NAME = os.getenv('SERVICE_NAME', 'Notification Channels Service')