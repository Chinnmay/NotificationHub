"""
Tests for EventTransformer
"""

import pytest
from unittest.mock import patch

from app.core.transformer import EventTransformer


class TestEventTransformer:
    """Test cases for EventTransformer"""
    
    @pytest.fixture
    def transformer(self):
        """Create EventTransformer instance for testing"""
        return EventTransformer()
    
    def test_transformer_initialization(self, transformer):
        """Test transformer initialization"""
        assert transformer.routing_rules is not None
        assert len(transformer.routing_rules) > 0
    
    def test_transform_event_valid(self, transformer):
        """Test transforming a valid event"""
        message = {
            'topic': 'order.events',
            'data': {
                'event_type': 'order.created',
                'user_id': 'user123',
                'order_id': 'order456',
                'amount': 99.99
            }
        }
        
        notifications = transformer.transform_event(message)
        
        assert len(notifications) == 2  # email and push
        assert notifications[0]['user_id'] == 'user123'
        assert notifications[0]['event_type'] == 'order.created'
        assert notifications[0]['channel'] in ['email', 'push']
    
    def test_transform_event_invalid_user_id(self, transformer):
        """Test transforming event with missing user_id"""
        message = {
            'topic': 'order.events',
            'data': {
                'event_type': 'order.created',
                'order_id': 'order456'
            }
        }
        
        notifications = transformer.transform_event(message)
        
        assert len(notifications) == 0
    
    def test_transform_event_invalid_event_type(self, transformer):
        """Test transforming event with invalid event_type"""
        message = {
            'topic': 'order.events',
            'data': {
                'event_type': 'invalid.event',
                'user_id': 'user123'
            }
        }
        
        notifications = transformer.transform_event(message)
        
        assert len(notifications) == 0
    
    def test_create_notification(self, transformer):
        """Test creating a notification"""
        notification = transformer._create_notification(
            user_id='user123',
            channel='email',
            event_type='order.created',
            data={'order_id': 'order456'},
            source_topic='order.events'
        )
        
        assert notification is not None
        assert notification['user_id'] == 'user123'
        assert notification['channel'] == 'email'
        assert notification['event_type'] == 'order.created'
        assert notification['priority'] in [1, 2, 3]
        assert notification['status'] == 'pending'
    
    def test_enrich_event_data(self, transformer):
        """Test enriching event data"""
        data = {'order_id': 'order456', 'amount': 99.99}
        
        enriched = transformer._enrich_event_data('order.created', 'user123', data)
        
        assert enriched['user_id'] == 'user123'
        assert enriched['event_type'] == 'order.created'
        assert 'order_summary' in enriched
        assert 'action_url' in enriched
    
    def test_get_notification_priority(self, transformer):
        """Test getting notification priority"""
        # High priority
        assert transformer._get_notification_priority('payment.failed') == 3
        
        # Medium priority
        assert transformer._get_notification_priority('order.created') == 2
        
        # Low priority
        assert transformer._get_notification_priority('user.registered') == 1
    
    def test_get_supported_event_types(self, transformer):
        """Test getting supported event types"""
        event_types = transformer.get_supported_event_types()
        
        assert len(event_types) > 0
        assert 'order.created' in event_types
        assert 'payment.success' in event_types
    
    def test_get_supported_channels(self, transformer):
        """Test getting supported channels"""
        channels = transformer.get_supported_channels()
        
        assert len(channels) > 0
        assert 'email' in channels
        assert 'sms' in channels
        assert 'push' in channels
    
    def test_add_routing_rule(self, transformer):
        """Test adding a routing rule"""
        success = transformer.add_routing_rule('test.event', ['email'])
        
        assert success is True
        assert 'test.event' in transformer.routing_rules
        assert transformer.routing_rules['test.event'] == ['email']
