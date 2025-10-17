"""
Configuration management for end-to-end integration tests

This module provides test configuration settings that align with the current
system configuration, ensuring tests validate the actual production behavior
of the notification processing pipeline.
"""

import os
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class E2ETestConfig:
    """Configuration settings for end-to-end integration tests
    
    This configuration class ensures test settings align with the current
    system configuration including Kafka topics, routing rules, and
    consumer group settings.
    """
    
    # Kafka settings (matching current system)
    kafka_bootstrap_servers: str = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9094')
    
    # Test timeouts
    test_timeout: int = int(os.getenv('TEST_TIMEOUT', '30'))  # seconds
    message_timeout: int = int(os.getenv('MESSAGE_TIMEOUT', '10'))  # seconds per message
    consumer_startup_wait: int = int(os.getenv('CONSUMER_STARTUP_WAIT', '5'))  # seconds
    
    # Test consumer group prefix (to avoid conflicts)
    test_consumer_group_prefix: str = 'e2e-test'
    
    # Input topics (Core Service consumes from these)
    input_topics: Dict[str, str] = None
    
    # Output topics (Core Service produces to these, Channels Service consumes)
    output_topics: Dict[str, str] = None
    
    # Expected routing rules (matching Core Service settings)
    expected_routing: Dict[str, List[str]] = None
    
    # Test data settings
    test_user_prefix: str = 'e2e_test_user'
    test_order_prefix: str = 'e2e_test_order'
    test_payment_prefix: str = 'e2e_test_payment'
    
    def __post_init__(self):
        if self.input_topics is None:
            # Input topics that the Core Service consumes from
            self.input_topics = {
                'order_events': 'order.events',
                'payment_events': 'payment.events',
                'user_events': 'user.events'
            }
        
        if self.output_topics is None:
            # Output topics that the Channels Service consumes from
            self.output_topics = {
                'email': 'notifications.email',
                'sms': 'notifications.sms',
                'webhook': 'notifications.webhook',
                'slack': 'notifications.slack'
                # Note: 'push' topic exists in Core Service but no corresponding consumer
            }
        
        if self.expected_routing is None:
            # Routing rules that match the Core Service configuration
            self.expected_routing = {
                'order.created': ['email', 'push'],  # push notifications not processed by channels service
                'order.cancelled': ['email', 'sms'],
                'payment.success': ['email', 'push'],  # push notifications not processed by channels service
                'payment.failed': ['email', 'sms'],
                'user.registered': ['email']
            }

# Global test configuration instance for E2E tests
test_config = E2ETestConfig()