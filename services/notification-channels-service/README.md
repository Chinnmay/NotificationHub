# Notification Channels Service

A multi-consumer service that processes notifications from Kafka and delivers them through various channels. Each channel runs as an independent consumer for optimal performance and scalability.

## 🎯 Purpose

This service handles the final step in the notification pipeline:
- Consumes notifications from channel-specific Kafka topics
- Processes notifications for each channel type
- Delivers notifications through appropriate delivery mechanisms
- Provides independent scaling for each channel

## 🏗️ Architecture

```
Core Service ──▶ Kafka Topics ──▶ Channel Consumers ──▶ Notification Delivery
                    │                    │                      │
              notifications.email    Email Consumer        Email Service
              notifications.sms      SMS Consumer          SMS Provider  
              notifications.webhook  Webhook Consumer      HTTP Endpoints
              notifications.slack    Slack Consumer        Slack API
```

## 📁 Service Structure

```
notification-channels-service/
├── consumers/                   # Channel-specific consumers
│   ├── email_consumer.py       # Email notification processing
│   ├── sms_consumer.py         # SMS notification processing
│   ├── webhook_consumer.py     # Webhook notification processing
│   └── slack_consumer.py       # Slack notification processing
├── common/                     # Shared utilities
│   ├── config.py              # Configuration management
│   ├── kafka_utils.py         # Kafka utility functions
│   └── __init__.py            # Package exports
├── config.env                 # Environment configuration
├── docker-compose.yml         # Multi-container deployment
├── Dockerfile                 # Container image
└── requirements.txt           # Python dependencies
```

## 📋 Supported Channels

### 📧 Email Consumer
- **Topic**: `notifications.email`
- **Consumer Group**: `notification-email`
- **Processing**: HTML email generation, subject templates
- **Output**: Console logging (demo implementation)

### 📱 SMS Consumer
- **Topic**: `notifications.sms`
- **Consumer Group**: `notification-sms`
- **Processing**: SMS message templates, phone formatting
- **Output**: Console logging (demo implementation)

### 🔗 Webhook Consumer
- **Topic**: `notifications.webhook`
- **Consumer Group**: `notification-webhook`
- **Processing**: HTTP POST requests, JSON payloads
- **Output**: Console logging (demo implementation)

### 💬 Slack Consumer
- **Topic**: `notifications.slack`
- **Consumer Group**: `notification-slack`
- **Processing**: Slack message formatting, channel routing
- **Output**: Console logging (demo implementation)

## ⚙️ Configuration

### Environment Variables

Create a `config.env` file:

```env
# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9094
KAFKA_CONSUMER_GROUP_PREFIX=notification

# Topic Configuration
KAFKA_TOPIC_EMAIL=notifications.email
KAFKA_TOPIC_SMS=notifications.sms
KAFKA_TOPIC_WEBHOOK=notifications.webhook
KAFKA_TOPIC_SLACK=notifications.slack

# Channel Processing Delays (milliseconds)
EMAIL_DELAY_MS=100
SMS_DELAY_MS=150
WEBHOOK_DELAY_MS=200
SLACK_DELAY_MS=120

# Service Configuration
LOG_LEVEL=INFO
SERVICE_NAME=Notification Channels Service
```

### Kafka Topics

The service consumes from these topics:

| Topic | Consumer Group | Purpose |
|-------|---------------|---------|
| `notifications.email` | `notification-email` | Email notifications |
| `notifications.sms` | `notification-sms` | SMS notifications |
| `notifications.webhook` | `notification-webhook` | Webhook notifications |
| `notifications.slack` | `notification-slack` | Slack notifications |

## 🚀 Running the Service

### Prerequisites

- Kafka cluster running on `localhost:9094`
- Docker and Docker Compose
- Core Service running and producing notifications

### Option 1: Docker Compose (Recommended)

```bash
cd services/notification-channels-service

# Start all consumers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Option 2: Individual Consumers

```bash
# Install dependencies
pip install -r requirements.txt

# Run individual consumers
python consumers/email_consumer.py
python consumers/sms_consumer.py
python consumers/webhook_consumer.py
python consumers/slack_consumer.py
```

### Option 3: Background Processes

```bash
# Start all consumers in background
nohup python consumers/email_consumer.py &
nohup python consumers/sms_consumer.py &
nohup python consumers/webhook_consumer.py &
nohup python consumers/slack_consumer.py &
```

## 🔧 Consumer Management

### Start Specific Consumer

```bash
# Start only email consumer
docker-compose up -d email-consumer

# Start email and SMS consumers
docker-compose up -d email-consumer sms-consumer
```

### Stop Consumers

```bash
# Stop all consumers
docker-compose down

# Stop specific consumer
docker-compose stop email-consumer
```

### Restart Consumer

```bash
# Restart email consumer
docker-compose restart email-consumer

# Restart with fresh logs
docker-compose up -d --force-recreate email-consumer
```

## 📊 Monitoring

### Container Status

```bash
# Check all containers
docker-compose ps

# Check specific container logs
docker-compose logs email-consumer
```

### Kafka Consumer Groups

```bash
# Check consumer group status
cd ../../kafka-local/scripts
./consumer.sh notifications.email
```

### Processing Logs

Each consumer logs:
- Message consumption events
- Processing status
- Delivery confirmations
- Error conditions

## 🧪 Testing

### Manual Testing

```bash
# Send test notification to email topic
cd ../../kafka-local/scripts
./producer.sh notifications.email '{
    "notification_id": "test_123",
    "user_id": "user_456",
    "channel": "email",
    "event_type": "order.created",
    "data": {
        "subject": "Test Email",
        "body": "This is a test notification"
    }
}'
```

### Integration Testing

```bash
# Run end-to-end tests from project root
cd tests
python run_e2e_test.py
```

## 🔧 Development

### Adding New Channel

1. **Create consumer file**:
```bash
# Copy existing consumer as template
cp consumers/email_consumer.py consumers/new_channel_consumer.py
```

2. **Update configuration**:
```python
# Add to common/config.py
KAFKA_TOPIC_NEW_CHANNEL = os.getenv('KAFKA_TOPIC_NEW_CHANNEL', 'notifications.new_channel')
NEW_CHANNEL_DELAY_MS = int(os.getenv('NEW_CHANNEL_DELAY_MS', '100'))
```

3. **Update Docker Compose**:
```yaml
# Add to docker-compose.yml
new-channel-consumer:
  build: .
  container_name: notification-new-channel-consumer
  command: ["python", "consumers/new_channel_consumer.py"]
  network_mode: host
  env_file:
    - config.env
```

4. **Update Core Service routing** to include new channel

### Customizing Channel Logic

Each consumer can be customized:

```python
async def send_notification(notification: Dict[str, Any]) -> bool:
    """Custom notification delivery logic"""
    try:
        # Extract notification data
        user_id = notification.get('user_id')
        data = notification.get('data', {})
        
        # Custom processing logic
        message = format_message(data)
        
        # Custom delivery mechanism
        await deliver_to_channel(user_id, message)
        
        return True
    except Exception as e:
        print(f"❌ Delivery failed: {e}")
        return False
```

## 🚨 Troubleshooting

### Consumer Not Processing Messages

```bash
# Check consumer group offsets
cd ../../kafka-local/scripts
./consumer.sh notifications.email

# Reset consumer group if needed
kafka-consumer-groups --bootstrap-server localhost:9092 \
  --group notification-email \
  --topic notifications.email \
  --reset-offsets --to-earliest --execute
```

### High Memory Usage

```bash
# Monitor container resources
docker stats

# Restart containers if needed
docker-compose restart
```

### Connection Issues

```bash
# Check Kafka connectivity
docker-compose -f ../../kafka-local/docker-compose.yml ps

# Verify topic existence
cd ../../kafka-local/scripts
./topics.sh
```

## 🔄 Integration

This service integrates with:
- **Core Service**: Consumes notifications from topics
- **Kafka**: Message queuing and delivery
- **External Services**: Notification delivery endpoints (when implemented)

## 🎯 Design Principles

1. **Independent Consumers**: Each channel scales independently
2. **Simple & Focused**: Minimal code, maximum clarity
3. **Configurable**: Easy to modify behavior via environment
4. **Observable**: Comprehensive logging for monitoring
5. **Reliable**: Graceful error handling and recovery