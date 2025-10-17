# NotificationHub

A comprehensive notification processing system built with Python, FastAPI, and Kafka for scalable, real-time event-driven notifications across multiple channels.

## 🏗️ System Architecture

NotificationHub consists of two main services that work together to process events and deliver notifications:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Event Sources │───▶│  Core Service   │───▶│ Channels Service│
│ (order, payment,│    │ (transformation │    │ (email, sms,    │
│ user events)    │    │ & routing)      │    │ webhook, slack) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Kafka Topics  │    │  Notification   │
                       │ (input events)  │    │    Delivery     │
                       └─────────────────┘    └─────────────────┘
```

### 🔄 How It Works

1. **Event Ingestion**: External systems send events (orders, payments, user actions) to Kafka input topics
2. **Event Processing**: Core Service consumes events, transforms them into notifications, and applies routing rules
3. **Notification Delivery**: Channels Service consumes notifications and delivers them through appropriate channels
4. **Multi-Channel Support**: Each notification channel (email, SMS, webhook, Slack) runs as an independent consumer

## 📁 Project Structure

```
NotificationHub/
├── main.py                                    # Main application entry point
├── requirements.txt                           # Python dependencies
├── kafka-local/                              # Local Kafka setup
│   ├── docker-compose.yml                    # Kafka cluster configuration
│   └── scripts/                              # Kafka management scripts
├── services/
│   ├── notification-core-service/            # Event processing service
│   │   ├── app/
│   │   │   ├── main.py                       # Core service entry point
│   │   │   ├── core/                         # Business logic components
│   │   │   │   ├── consumer.py               # Kafka event consumer
│   │   │   │   ├── producer.py               # Kafka notification producer
│   │   │   │   └── transformer.py            # Event-to-notification transformer
│   │   │   ├── config/                       # Configuration management
│   │   │   └── utils/                        # Utility functions
│   │   ├── config.env                        # Service configuration
│   │   └── requirements.txt                  # Service dependencies
│   └── notification-channels-service/        # Notification delivery service
│       ├── consumers/                        # Channel-specific consumers
│       │   ├── email_consumer.py             # Email notification consumer
│       │   ├── sms_consumer.py               # SMS notification consumer
│       │   ├── webhook_consumer.py           # Webhook notification consumer
│       │   └── slack_consumer.py             # Slack notification consumer
│       ├── common/                           # Shared utilities
│       ├── config.env                        # Service configuration
│       ├── docker-compose.yml                # Multi-container setup
│       └── requirements.txt                  # Service dependencies
└── tests/                                    # Integration tests
    ├── e2e/                                  # End-to-end tests
    ├── run_e2e_test.py                       # Test runner
    └── requirements.txt                      # Test dependencies
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (for Kafka)
- **Python 3.10+**
- **Git**

### 1. Clone and Setup

```bash
git clone <repository-url>
cd NotificationHub

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install main dependencies
pip install -r requirements.txt
```

### 2. Start Kafka Cluster

```bash
cd kafka-local
docker-compose up -d
```

This starts:
- Zookeeper (port 2181)
- Kafka broker (port 9094)
- Kafka UI (port 8080)

### 3. Start Core Service

```bash
cd services/notification-core-service
pip install -r requirements.txt
python app/main.py
```

### 4. Start Channels Service

```bash
cd services/notification-channels-service
pip install -r requirements.txt
docker-compose up -d
```

This starts all notification consumers:
- Email consumer
- SMS consumer  
- Webhook consumer
- Slack consumer

### 5. Verify System

```bash
# Run integration tests
cd tests
pip install -r requirements.txt
python run_e2e_test.py
```

## 🔧 Configuration

### Kafka Topics

The system uses these Kafka topics:

**Input Topics (Core Service consumes):**
- `order.events` - Order-related events
- `payment.events` - Payment-related events  
- `user.events` - User-related events

**Output Topics (Channels Service consumes):**
- `notifications.email` - Email notifications
- `notifications.sms` - SMS notifications
- `notifications.webhook` - Webhook notifications
- `notifications.slack` - Slack notifications

### Event Routing Rules

| Event Type | Channels |
|------------|----------|
| `order.created` | email, webhook, slack |
| `order.cancelled` | email, sms |
| `payment.success` | email |
| `payment.failed` | email, sms |
| `user.registered` | email |

## 📊 Monitoring

### Service Health

- **Core Service**: Check logs for event processing
- **Channels Service**: Check Docker container status
- **Kafka**: Access Kafka UI at http://localhost:8080

### Logs

```bash
# Core Service logs
tail -f services/notification-core-service/logs/app.log

# Channels Service logs
docker-compose -f services/notification-channels-service/docker-compose.yml logs -f
```

## 🧪 Testing

### Integration Tests

```bash
cd tests
python run_e2e_test.py
```

Tests verify:
- Event ingestion from input topics
- Event transformation and routing
- Notification delivery through all channels
- End-to-end message flow

### Manual Testing

```bash
# Send test events to Kafka
cd kafka-local/scripts
./producer.sh order.events '{"event_type":"order.created","user_id":"test123","order_id":"ORD001","amount":99.99}'
```

## 🛠️ Development

### Adding New Channels

1. Create consumer in `services/notification-channels-service/consumers/`
2. Add topic configuration in `common/config.py`
3. Update routing rules in Core Service
4. Add to Docker Compose configuration

### Adding New Event Types

1. Update routing rules in `services/notification-core-service/app/config/settings.py`
2. Test with integration tests
3. Update documentation

## 🔍 Troubleshooting

### Common Issues

**Kafka Connection Failed**
```bash
# Check Kafka status
docker-compose -f kafka-local/docker-compose.yml ps

# Check logs
docker-compose -f kafka-local/docker-compose.yml logs kafka
```

**Messages Not Consumed**
```bash
# Check consumer group offsets
cd kafka-local/scripts
./consumer.sh notifications.email
```

**Services Not Starting**
```bash
# Check dependencies
pip install -r requirements.txt

# Check configuration
cat services/*/config.env
```

## 📈 Performance

- **Throughput**: Handles thousands of events per second
- **Latency**: Sub-second notification delivery
- **Scalability**: Horizontal scaling via Kafka partitioning
- **Reliability**: At-least-once delivery guarantees

## 🔒 Security

- Environment-based configuration
- Kafka SASL authentication support
- Input validation on all events
- Secure Docker container deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ using Python, FastAPI, and Kafka**