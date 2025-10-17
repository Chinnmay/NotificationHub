# Integration Tests

Comprehensive end-to-end integration tests for the notification system that validate
the complete pipeline from event ingestion to notification delivery across all channels.

## Project Structure

```
NotificationHub/
├── services/
│   ├── notification-core-service/
│   └── notification-channels-service/
├── kafka-local/
└── tests/                    # Integration tests at project root level
    ├── e2e/
    │   └── test_simple_e2e.py
    ├── test_config.py
    ├── requirements.txt
    ├── run_e2e_test.py
    └── README.md
```

## Prerequisites

Before running the integration tests, ensure the following services are operational:

1. **Kafka cluster** running on `localhost:9094`
2. **Core Service** running and processing events from input topics
3. **Channels Service** running with all consumer containers active

## Running Tests

### Execute Integration Tests
```bash
cd NotificationHub
python tests/run_e2e_test.py
```

### Direct Test
```bash
cd NotificationHub
python tests/e2e/test_simple_e2e.py
```

## What It Tests

- ✅ **Event Injection**: Sends events to input topics (`order.events`, `payment.events`, `user.events`)
- ✅ **Message Processing**: Monitors output topics for notifications
- ✅ **End-to-End Flow**: Verifies complete event → notification pipeline
- ✅ **Multiple Channels**: Tests email, SMS, webhook, slack processing

## Test Events

- `order.created` → should generate email notification
- `order.cancelled` → should generate email + SMS notifications  
- `payment.success` → should generate email notification
- `payment.failed` → should generate email + SMS notifications
- `user.registered` → should generate email notification
