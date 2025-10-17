"""
Tests for EventConsumer
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.core.consumer import EventConsumer


class TestEventConsumer:
    """Test cases for EventConsumer"""
    
    @pytest.fixture
    def consumer(self):
        """Create EventConsumer instance for testing"""
        return EventConsumer()
    
    def test_consumer_initialization(self, consumer):
        """Test consumer initialization"""
        assert consumer.consumer is None
        assert consumer.is_started is False
    
    @pytest.mark.asyncio
    async def test_start_consumer(self, consumer):
        """Test starting the consumer"""
        # Mock AIOKafkaConsumer
        with pytest.MonkeyPatch().context() as m:
            mock_consumer = AsyncMock()
            m.setattr("aiokafka.AIOKafkaConsumer", lambda **kwargs: mock_consumer)
            
            await consumer.start()
            
            assert consumer.is_started is True
            mock_consumer.start.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_stop_consumer(self, consumer):
        """Test stopping the consumer"""
        # Mock consumer
        consumer.consumer = AsyncMock()
        consumer.is_started = True
        
        await consumer.stop()
        
        assert consumer.is_started is False
        consumer.consumer.stop.assert_called_once()
    
    def test_deserialize_message(self, consumer):
        """Test message deserialization"""
        import json
        
        # Test valid JSON
        test_data = {"key": "value", "number": 123}
        message_bytes = json.dumps(test_data).encode('utf-8')
        
        result = consumer._deserialize_message(message_bytes)
        assert result == test_data
        
        # Test invalid JSON
        invalid_bytes = b"invalid json"
        result = consumer._deserialize_message(invalid_bytes)
        assert result == {}
    
    def test_is_ready(self, consumer):
        """Test is_ready method"""
        # Not ready initially
        assert consumer.is_ready() is False
        
        # Ready when started and consumer exists
        consumer.is_started = True
        consumer.consumer = MagicMock()
        assert consumer.is_ready() is True
