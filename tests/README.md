# Integration Tests

Comprehensive end-to-end integration tests that validate the complete notification processing pipeline from event ingestion to notification delivery.

## 🎯 Test Purpose

These tests verify:
- Event ingestion from input topics
- Event transformation and routing by Core Service
- Notification delivery through Channels Service
- End-to-end message flow integrity
- System reliability and performance

## 📁 Test Structure

```
tests/
├── e2e/
│   └── test_simple_e2e.py     # Main integration test
├── test_config.py             # Test configuration
├── run_e2e_test.py            # Test runner script
├── requirements.txt           # Test dependencies
└── README.md                  # This file
```

## 🚀 Running Tests

### Prerequisites

Ensure these services are running:

1. **Kafka Cluster** - `localhost:9094`
2. **Core Service** - Processing events from input topics
3. **Channels Service** - All consumer containers active

### Quick Test Run

```bash
# From project root
cd tests
python run_e2e_test.py
```

### Detailed Test Execution

```bash
# Install test dependencies
pip install -r requirements.txt

# Run with verbose output
python run_e2e_test.py

# Check test results
echo $?  # 0 = success, 1 = failure
```

## ⚙️ Test Configuration

Tests use configuration from `test_config.py`:

### Kafka Settings
```python
kafka_bootstrap_servers = 'localhost:9094'
test_consumer_group_prefix = 'e2e-test'
```

### Test Topics
```python
input_topics = {
    'order_events': 'order.events',
    'payment_events': 'payment.events', 
    'user_events': 'user.events'
}

output_topics = {
    'email': 'notifications.email',
    'sms': 'notifications.sms',
    'webhook': 'notifications.webhook',
    'slack': 'notifications.slack'
}
```

### Expected Routing
```python
expected_routing = {
    'order.created': ['email', 'webhook', 'slack'],
    'order.cancelled': ['email', 'sms'],
    'payment.success': ['email'],
    'payment.failed': ['email', 'sms'],
    'user.registered': ['email']
}
```

## 📊 Test Flow

### 1. Setup Phase
- Connect to Kafka cluster
- Create test producer
- Initialize output topic consumers
- Verify service connectivity

### 2. Test Execution
- Generate test events
- Send events to input topics
- Monitor output topics for notifications
- Track message processing

### 3. Verification
- Validate all expected notifications received
- Check notification content accuracy
- Verify routing rules followed
- Confirm processing timeliness

### 4. Cleanup
- Close Kafka connections
- Report test results
- Clean up test data

## 📝 Test Events

The test generates realistic events:

### Order Events
```json
{
  "event_id": "evt_001",
  "event_type": "order.created",
  "user_id": "test_user_001",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "order_id": "ORD_001",
    "amount": 99.99,
    "items": ["product1", "product2"]
  }
}
```

### Payment Events
```json
{
  "event_id": "evt_002", 
  "event_type": "payment.success",
  "user_id": "test_user_002",
  "timestamp": "2024-01-15T10:31:00Z",
  "data": {
    "payment_id": "PAY_001",
    "amount": 99.99,
    "method": "credit_card"
  }
}
```

## ✅ Expected Results

### Successful Test Output
```
🧪 Running End-to-End Integration Test...
📋 Prerequisites:
  ✅ Kafka running on localhost:9094
  ✅ Core Service running and processing events
  ✅ Channels Service running and processing notifications

🚀 Starting E2E test environment...
✅ Producer connected
✅ Consumer connected to notifications.email
✅ Consumer connected to notifications.sms
📤 Sending 5 events...
📤 Sent order.created to order.events
📤 Sent order.cancelled to order.events
📥 Received order.created from notifications.email
📥 Received order.cancelled from notifications.sms
✅ Received sufficient notifications
🎉 E2E Test PASSED!
```

### Test Metrics
- **Events Sent**: 5
- **Notifications Received**: 5
- **Processing Time**: < 30 seconds
- **Success Rate**: 100%

## 🚨 Troubleshooting

### Common Issues

**No notifications received:**
```bash
# Check Core Service status
ps aux | grep python | grep main

# Verify Kafka topics
cd ../kafka-local/scripts
./topics.sh
```

**Consumer group conflicts:**
```bash
# Reset consumer groups
kafka-consumer-groups --bootstrap-server localhost:9092 \
  --group e2e-test-email --reset-offsets --to-earliest --execute
```

**Timeout errors:**
```bash
# Increase timeout in test_config.py
test_timeout = 60  # seconds
```

### Debug Mode

Enable detailed logging:

```bash
export LOG_LEVEL=DEBUG
python run_e2e_test.py
```

### Manual Verification

```bash
# Send test message manually
cd ../kafka-local/scripts
./producer.sh order.events '{"event_type":"order.created","user_id":"test123"}'

# Check consumer logs
docker-compose -f ../services/notification-channels-service/docker-compose.yml logs email-consumer
```

## 🔧 Customizing Tests

### Adding New Event Types

1. **Update routing rules** in `test_config.py`:
```python
expected_routing['inventory.low'] = ['email', 'sms']
```

2. **Add test data generation**:
```python
def create_inventory_event():
    return {
        "event_type": "inventory.low",
        "user_id": "admin_user",
        "data": {"product_id": "PROD_123", "quantity": 5}
    }
```

### Adding New Channels

1. **Update output topics** in configuration
2. **Add consumer monitoring** to test
3. **Update expected routing** rules

## 📈 Performance Testing

For load testing, modify test configuration:

```python
# Increase test load
test_events_count = 100
message_send_delay = 0.01  # seconds
```

## 🔄 CI/CD Integration

Tests can be integrated into deployment pipelines:

```yaml
# Example GitHub Actions step
- name: Run Integration Tests
  run: |
    cd tests
    pip install -r requirements.txt
    python run_e2e_test.py
```

---

**Note**: These tests require all services to be running and properly configured. Ensure Kafka and both notification services are operational before running tests.