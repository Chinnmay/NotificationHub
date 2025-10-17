# Notification Core Service

A clean, focused service that consumes events from Kafka and transforms them into notifications for different channels (email, SMS, push).

## 🏗️ Architecture

```
notification-core-service/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # entrypoint — starts the Kafka consumer loop
│   │
│   ├── core/                   # core logic: consume, process, produce
│   │   ├── __init__.py
│   │   ├── consumer.py         # Kafka consumer operations
│   │   ├── producer.py         # Kafka producer operations
│   │   └── transformer.py      # Event transformation logic
│   │
│   ├── config/                 # settings and configs
│   │   ├── __init__.py
│   │   └── settings.py         # Configuration management
│   │
│   └── utils/                  # helper stuff (logger, common utils)
│       ├── __init__.py
│       └── logger.py           # Logging utilities
│
├── tests/
│   ├── __init__.py
│   ├── test_consumer.py        # Consumer tests
│   ├── test_producer.py        # Producer tests
│   └── test_transformer.py     # Transformer tests
│
├── requirements.txt
├── Dockerfile
├── config.env                  # Environment variables template
└── README.md
```

## 🚀 Features

- **Event Processing**: Consumes events from Kafka topics
- **Smart Routing**: Transforms events into notifications based on routing rules
- **Multi-Channel**: Supports email, SMS, and push notifications
- **Clean Architecture**: Focused, single-responsibility modules
- **Async Processing**: High-performance async Kafka operations
- **Graceful Shutdown**: Proper signal handling for clean shutdowns

## 📋 Supported Event Types

- `order.created` → Email + Push notification
- `order.cancelled` → Email + SMS notification
- `payment.success` → Email + Push notification
- `payment.failed` → Email + SMS notification
- `user.registered` → Welcome email

## 📨 Output Channels

- **Email**: `notifications.email` topic
- **SMS**: `notifications.sms` topic
- **Push**: `notifications.push` topic

## 🛠️ Running the Service

### Prerequisites

1. **Kafka**: Make sure Kafka is running on `localhost:9094`
2. **Python**: Python 3.10+
3. **Dependencies**: Install requirements

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp config.env .env
```

### Running

```bash
# Run directly
python -m app.main

# Or run the main module
python app/main.py
```

### Docker

```bash
# Build image
docker build -t notification-core-service .

# Run container
docker run -d --name notification-service notification-core-service
```

## ⚙️ Configuration

Configuration is managed through environment variables and the `config/settings.py` file:

### Environment Variables

- `KAFKA_BOOTSTRAP_SERVERS`: Kafka servers (default: `localhost:9094`)
- `KAFKA_CONSUMER_GROUP`: Consumer group ID (default: `notification-core`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

### Settings

The service uses a centralized settings system:

```python
# Routing rules
ROUTING_RULES = {
    'order.created': ['email', 'push'],
    'payment.success': ['email', 'push'],
    # ... more rules
}

# Channel topics
CHANNEL_TOPICS = {
    'email': 'notifications.email',
    'sms': 'notifications.sms',
    'push': 'notifications.push'
}
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_transformer.py

# Run with coverage
pytest --cov=app tests/
```

## 🔧 Development

### Adding New Event Types

1. Add routing rule in `config/settings.py`:
```python
ROUTING_RULES['new.event'] = ['email', 'sms']
```

2. Add enrichment logic in `core/transformer.py`:
```python
def _enrich_event_data(self, event_type, user_id, data):
    # ... existing logic
    elif event_type == "new.event":
        enriched_data.update({
            "custom_field": "custom_value"
        })
```

### Adding New Channels

1. Add channel topic in `config/settings.py`:
```python
CHANNEL_TOPICS['new_channel'] = 'notifications.new_channel'
```

2. Update routing rules to use the new channel

## 📊 Monitoring

The service provides structured logging for monitoring:

- **Event Processing**: Logs when events are processed
- **Notification Sending**: Logs successful/failed notifications
- **Errors**: Detailed error logging with context
- **Service Lifecycle**: Startup/shutdown events

## 🎯 Design Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Clean Architecture**: Clear separation of concerns
3. **Async First**: All I/O operations are async
4. **Configurable**: Easy to modify behavior via configuration
5. **Testable**: Comprehensive test coverage
6. **Production Ready**: Proper error handling and logging

## 🔄 Data Flow

1. **Consumer** receives events from Kafka topics
2. **Transformer** processes events and creates notifications
3. **Producer** sends notifications to channel-specific topics
4. **Logger** records all operations for monitoring

This service is designed to be **simple, focused, and reliable** - perfect for a single microservice responsibility!
