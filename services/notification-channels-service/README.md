# Notification Channels Service

A multi-consumer service that processes notifications from Kafka and sends them through various channels (email, SMS, webhook, Slack). Each channel runs as a separate consumer group for independent scaling and processing.

## 🏗️ Architecture

```
notification-channels-service/
├── consumers/               # Notification channel consumers
│   ├── __init__.py         # Consumers package exports
│   ├── email_consumer.py   # Email notification consumer
│   ├── sms_consumer.py     # SMS notification consumer  
│   ├── webhook_consumer.py # Webhook notification consumer
│   └── slack_consumer.py   # Slack notification consumer
├── common/                  # Shared utilities
│   ├── __init__.py         # Common package exports
│   ├── kafka_utils.py      # Simple Kafka utilities
│   └── config.py           # Simple configuration
├── requirements.txt         # Python dependencies
├── config.env              # Environment configuration
├── Dockerfile              # Container image
├── docker-compose.yml      # Multi-container setup
└── README.md               # This file
```

## 🚀 Features

- **Multi-Channel Support**: Email, SMS, Webhook, Slack
- **Independent Consumers**: Each channel runs as separate consumer group
- **Simple & Clean**: Minimal, focused codebase (~430 lines total)
- **Docker Ready**: Multi-container deployment
- **Graceful Shutdown**: Proper signal handling
- **Easy Configuration**: Simple environment-based configuration

## 📋 Supported Channels

### 📧 Email Consumer
- **Topic**: `notifications.email`
- **Consumer Group**: `notification-email`
- **Features**: HTML email generation, subject/body templates

### 📱 SMS Consumer  
- **Topic**: `notifications.sms`
- **Consumer Group**: `notification-sms`
- **Features**: SMS message templates, phone number lookup

### 🔗 Webhook Consumer
- **Topic**: `notifications.webhook`
- **Consumer Group**: `notification-webhook`
- **Features**: HTTP POST requests, JSON payloads

### 💬 Slack Consumer
- **Topic**: `notifications.slack`
- **Consumer Group**: `notification-slack`
- **Features**: Rich message blocks, channel routing

## 🛠️ Running the Service

### Prerequisites

1. **External Kafka**: Make sure the Kafka service from `kafka-local/` is running on `localhost:9094`
   ```bash
   cd kafka-local && docker-compose up -d
   ```
2. **Python**: Python 3.10+
3. **Dependencies**: Install requirements

### Individual Consumers

```bash
# Run individual consumers
python consumers/email_consumer.py
python consumers/sms_consumer.py
python consumers/webhook_consumer.py
python consumers/slack_consumer.py
```

### Docker Compose (All Consumers)

**Important**: Make sure the external Kafka service is running first:
```bash
# Start external Kafka service
cd ../kafka-local && docker-compose up -d

# Then start notification channels
cd ../notification-channels-service
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all
docker-compose down
```

### Individual Docker Containers

**Important**: Make sure the external Kafka service is running first:
```bash
# Start external Kafka service
cd ../kafka-local && docker-compose up -d

# Build image
docker build -t notification-channels-service .

# Run individual consumers
docker run -d --name email-consumer --network host notification-channels-service python consumers/email_consumer.py
docker run -d --name sms-consumer --network host notification-channels-service python consumers/sms_consumer.py
docker run -d --name webhook-consumer --network host notification-channels-service python consumers/webhook_consumer.py
docker run -d --name slack-consumer --network host notification-channels-service python consumers/slack_consumer.py
```

## ⚙️ Configuration

### Environment Variables

- `KAFKA_BOOTSTRAP_SERVERS`: Kafka servers (default: `localhost:9094`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

### External Kafka Dependency

The notification-channels-service expects an external Kafka service to be running. This should be the Kafka instance from the `kafka-local/` folder:

- **Kafka Container**: `notification-hub-kafka`
- **External Port**: `localhost:9094`
- **Auto Topic Creation**: Enabled (`KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'`)

**Start Kafka first:**
```bash
cd ../kafka-local
docker-compose up -d
```


## 📊 Logging

Structured logging with:
- Consumer startup/shutdown events
- Message processing success/failure
- Retry attempts and delays
- Error details and stack traces

## ⚙️ Configuration

Simple configuration through environment variables in `config.env`:

### Essential Configuration
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker addresses (default: localhost:9094)
- `KAFKA_TOPIC_EMAIL`: Email topic name (default: notifications.email)
- `KAFKA_TOPIC_SMS`: SMS topic name (default: notifications.sms)
- `KAFKA_TOPIC_WEBHOOK`: Webhook topic name (default: notifications.webhook)
- `KAFKA_TOPIC_SLACK`: Slack topic name (default: notifications.slack)

### Channel Delays
- `EMAIL_DELAY_MS`: Email simulation delay (default: 100ms)
- `SMS_DELAY_MS`: SMS simulation delay (default: 150ms)
- `WEBHOOK_DELAY_MS`: Webhook simulation delay (default: 200ms)
- `SLACK_DELAY_MS`: Slack simulation delay (default: 120ms)

**To change Kafka server:**
```bash
# Edit config.env
KAFKA_BOOTSTRAP_SERVERS=your-kafka-server:9092

# Or override via environment
export KAFKA_BOOTSTRAP_SERVERS=your-kafka-server:9092
```

## 🔧 Architecture

### Simple & Direct Design
- **Direct AIOKafkaConsumer usage** in each consumer
- **Simple configuration** with environment variables
- **Minimal abstractions** - no unnecessary base classes
- **Clear separation** - each consumer is self-contained

### Key Components
- **config.py**: Simple configuration constants
- **kafka_utils.py**: Basic utility functions
- **consumers/**: Independent consumer scripts
- **config.env**: Environment configuration


## 📝 Message Format

### Input (from Kafka)

```json
{
  "notification_id": "uuid",
  "user_id": "user123",
  "channel": "email",
  "event_type": "order.created",
  "data": {
    "order_id": "order456",
    "amount": 99.99,
    "order_summary": "Order #order456 has been created",
    "action_url": "/orders/order456"
  },
  "priority": 2,
  "status": "pending",
  "created_at": "2025-10-14T04:30:00Z"
}
```

### Channel-Specific Processing

Each channel extracts relevant data and formats it appropriately:

- **Email**: Subject, HTML body, recipient email
- **SMS**: Text message, recipient phone
- **Webhook**: JSON payload, webhook URL
- **Slack**: Rich blocks, channel routing

## 🎯 Design Benefits

1. **Independent Scaling**: Each channel can be scaled separately
2. **Fault Isolation**: Channel failures don't affect others
3. **Technology Flexibility**: Different channels can use different technologies
4. **Consumer Groups**: Kafka consumer groups for load balancing
5. **Shared Libraries**: Common utilities reduce code duplication
6. **Docker Ready**: Easy deployment and orchestration

## 🔄 Data Flow

```
Kafka Topics → Channel Consumers → Processing → Delivery
     ↓              ↓                ↓           ↓
notifications.  email_consumer   EmailProcessor  📧 Email
notifications.  sms_consumer    SMSProcessor    📱 SMS  
notifications.  webhook_consumer WebhookProcessor 🔗 Webhook
notifications.  slack_consumer  SlackProcessor  💬 Slack
```

Each consumer independently processes messages from its topic, applies channel-specific logic, and delivers notifications through the appropriate channel.

This architecture provides **high availability**, **scalability**, and **maintainability** for notification delivery! 🚀
