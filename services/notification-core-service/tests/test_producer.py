"""
Tests for NotificationProducer
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.core.producer import NotificationProducer


class TestNotificationProducer:
    """Test cases for NotificationProducer"""
    
    @pytest.fixture
    def producer(self):
        """Create NotificationProducer instance for testing"""
        return NotificationProducer()
    
    def test_producer_initialization(self, producer):
        """Test producer initialization"""
        assert producer.producer is None
        assert producer.is_started is False
    
    @pytest.mark.asyncio
    async def test_start_producer(self, producer):
        """Test starting the producer"""
        # Mock AIOKafkaProducer
        with pytest.MonkeyPatch().context() as m:
            mock_producer = AsyncMock()
            m.setattr("aiokafka.AIOKafkaProducer", lambda **kwargs: mock_producer)
            
            await producer.start()
            
            assert producer.is_started is True
            mock_producer.start.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_stop_producer(self, producer):
        """Test stopping the producer"""
        # Mock producer
        producer.producer = AsyncMock()
        producer.is_started = True
        
        await producer.stop()
        
        assert producer.is_started is False
        producer.producer.stop.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_send_message(self, producer):
        """Test sending a message"""
        # Mock producer
        mock_producer = AsyncMock()
        producer.producer = mock_producer
        producer.is_started = True
        
        test_topic = "test.topic"
        test_message = {"key": "value"}
        
        result = await producer.send_message(test_topic, test_message)
        
        assert result is True
        mock_producer.send_and_wait.assert_called_once_with(test_topic, test_message)
    
    @pytest.mark.asyncio
    async def test_send_notification(self, producer):
        """Test sending a notification"""
        # Mock producer
        mock_producer = AsyncMock()
        producer.producer = mock_producer
        producer.is_started = True
        
        test_channel = "email"
        test_notification = {"user_id": "123", "message": "test"}
        
        result = await producer.send_notification(test_channel, test_notification)
        
        assert result is True
        mock_producer.send_and_wait.assert_called_once()
    
    def test_is_ready(self, producer):
        """Test is_ready method"""
        # Not ready initially
        assert producer.is_ready() is False
        
        # Ready when started and producer exists
        producer.is_started = True
        producer.producer = MagicMock()
        assert producer.is_ready() is True
