# Notification Core Service

The central processing hub that consumes events from Kafka and transforms them into structured notifications for delivery through multiple channels.

## 🎯 Purpose

This service acts as the brain of the notification system, handling:
- Event consumption from various input topics
- Event transformation and enrichment
- Routing decisions based on event types
- Notification publishing to channel-specific topics

## 🏗️ Architecture

```
Input Events ──▶ Consumer ──▶ Transformer ──▶ Producer ──▶ Output Topics
     │              │            │            │            │
   Kafka         Event        Notification  Channel     Channels
  Topics        Processing    Generation   Routing     Service
```

## 📁 Service Structure

```
notification-core-service/
├── app/
│   ├── main.py                 # Service entry point
│   ├── core/                   # Core business logic
│   │   ├── consumer.py         # Kafka event consumer
│   │   ├── producer.py         # Kafka notification producer
│   │   └── transformer.py      # Event transformation engine
│   ├── config/                 # Configuration management
│   │   └── settings.py         # Service settings and routing rules
│   └── utils/                  # Utility functions
│       └── logger.py           # Logging configuration
├── tests/                      # Unit tests
├── config.env                  # Environment configuration
└── requirements.txt            # Python dependencies
```

## ⚙️ Configuration

### Environment Variables

Create a `config.env` file:

```env
# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9094
KAFKA_CONSUMER_GROUP=notification-core
KAFKA_AUTO_OFFSET_RESET=earliest

# Service Configuration
SERVICE_NAME=Notification Core Service
SERVICE_VERSION=2.0.0
LOG_LEVEL=INFO
```

### Routing Rules

Events are routed to channels based on these rules:

```python
ROUTING_RULES = {
    'order.created': ['email', 'webhook', 'slack'],
    'order.cancelled': ['email', 'sms'],
    'payment.success': ['email'],
    'payment.failed': ['email', 'sms'],
    'user.registered': ['email']
}
```

### Supported Topics

**Input Topics (consumes from):**
- `order.events` - Order-related events
- `payment.events` - Payment-related events
- `user.events` - User-related events

**Output Topics (produces to):**
- `notifications.email` - Email notifications
- `notifications.sms` - SMS notifications
- `notifications.webhook` - Webhook notifications
- `notifications.slack` - Slack notifications

## 🚀 Running the Service

### Prerequisites

- Kafka cluster running on `localhost:9094`
- Python 3.10+
- Virtual environment activated

### Installation

```bash
cd services/notification-core-service

# Install dependencies
pip install -r requirements.txt

# Copy configuration
cp config.env .env
```

### Start Service

```bash
# Run directly
python app/main.py

# Or as module
python -m app.main
```

### Docker (Optional)

```bash
# Build image
docker build -t notification-core-service .

# Run container
docker run -d --name notification-core-service notification-core-service
```

## 📊 Event Processing Flow

### 1. Event Consumption

```python
# Consumer receives events like:
{
    "event_id": "evt_123",
    "event_type": "order.created",
    "user_id": "user_456",
    "timestamp": "2024-01-15T10:30:00Z",
    "data": {
        "order_id": "ORD_789",
        "amount": 99.99,
        "items": ["item1", "item2"]
    }
}
```

### 2. Event Transformation

```python
# Transformer creates notifications like:
{
    "notification_id": "notif_abc",
    "user_id": "user_456",
    "channel": "email",
    "event_type": "order.created",
    "priority": 2,
    "status": "pending",
    "data": {
        "subject": "Order #ORD_789 Confirmed",
        "body": "Your order for $99.99 has been placed...",
        "order_id": "ORD_789"
    }
}
```

### 3. Notification Publishing

Notifications are published to channel-specific topics for the Channels Service to consume.

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_transformer.py -v

# Run with coverage
pytest --cov=app tests/
```

## 🔧 Development

### Adding New Event Types

1. **Update routing rules** in `config/settings.py`:
```python
ROUTING_RULES['inventory.low'] = ['email', 'sms']
```

2. **Add enrichment logic** in `core/transformer.py`:
```python
def _enrich_event_data(self, event_type, user_id, data):
    # ... existing logic
    elif event_type == "inventory.low":
        enriched_data.update({
            "alert_level": "high",
            "product_name": data.get("product_name")
        })
```

### Adding New Channels

1. **Add channel topic** in `config/settings.py`:
```python
CHANNEL_TOPICS['telegram'] = 'notifications.telegram'
```

2. **Update routing rules** to use the new channel
3. **Create corresponding consumer** in Channels Service

## 📈 Monitoring

### Logs

The service provides structured logging:

```bash
# View logs
tail -f logs/notification-core.log

# Filter by level
grep "ERROR" logs/notification-core.log
```

### Key Metrics

- Events processed per minute
- Notification generation rate
- Error rates by event type
- Processing latency

## 🚨 Troubleshooting

### Common Issues

**Kafka Connection Failed**
```bash
# Check Kafka status
docker-compose -f ../../kafka-local/docker-compose.yml ps
```

**No Events Being Processed**
```bash
# Check consumer group status
cd ../../kafka-local/scripts
./consumer.sh order.events
```

**High Memory Usage**
```bash
# Monitor memory
ps aux | grep python
# Adjust batch size in consumer configuration
```

## 🔄 Integration

This service integrates with:
- **Kafka**: For event consumption and notification publishing
- **Channels Service**: Provides notifications for delivery
- **External Systems**: Via Kafka topics for event ingestion

## 🎯 Design Principles

1. **Event-Driven**: Processes events asynchronously
2. **Stateless**: No persistent state, scalable horizontally
3. **Configurable**: Easy to modify routing rules
4. **Reliable**: At-least-once delivery guarantees
5. **Observable**: Comprehensive logging and monitoring