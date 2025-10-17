#!/bin/bash

# Kafka Producer Test Script
echo "📤 Kafka Producer Test..."

# Navigate to kafka-local directory
cd "$(dirname "$0")/.."

# Check if services are running
if ! docker-compose ps | grep -q "notification-hub-kafka.*Up"; then
    echo "❌ Kafka is not running. Please start it first with ./scripts/start.sh"
    exit 1
fi

TOPIC="${1:-notification-requests}"

echo "📤 Sending test messages to topic: $TOPIC"
echo "💡 Press Ctrl+C to stop"

docker-compose exec kafka kafka-console-producer \
    --topic "$TOPIC" \
    --bootstrap-server localhost:9092
