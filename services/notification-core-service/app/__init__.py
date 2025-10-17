"""
Notification Core Service

A comprehensive notification processing service that consumes events from Kafka
and transforms them into structured notifications for delivery through multiple
channels including email, SMS, webhooks, and Slack integrations.

Architecture:
- main.py: Application entry point and service orchestration
- core/: Core business logic (consumer, producer, transformer)
- config/: Configuration management and routing rules
- utils/: Utility functions and logging infrastructure
"""

from .main import main

__version__ = "2.0.0"
__all__ = ['main']
