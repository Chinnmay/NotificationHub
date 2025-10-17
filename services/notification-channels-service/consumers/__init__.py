"""
Notification channel consumers

This package contains Kafka consumers for different notification channels
including email, SMS, webhook, and Slack. Each consumer runs independently
and processes messages from its dedicated topic.
"""

# Consumer modules can be imported directly
__all__ = ['email_consumer', 'sms_consumer', 'webhook_consumer', 'slack_consumer']