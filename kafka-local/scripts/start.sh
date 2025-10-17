#!/bin/bash

# Start Kafka Local Environment (KRaft Mode)
echo "🚀 Starting Kafka Local Environment (KRaft Mode)..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Navigate to kafka-local directory
cd "$(dirname "$0")/.."

# Start services
echo "📦 Starting Kafka with KRaft..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for Kafka to be ready..."
sleep 15

# Check if Kafka is ready
echo "🔍 Checking Kafka health..."
for i in {1..30}; do
    if docker-compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1; then
        echo "✅ Kafka is ready!"
        break
    fi
    echo "⏳ Waiting for Kafka... ($i/30)"
    sleep 2
done

echo "🎉 Kafka Local Environment (KRaft) is ready!"
echo ""
echo "📊 Services:"
echo "  - Kafka (KRaft): localhost:9092"
echo "  - Kafka UI: http://localhost:8080"
echo ""
echo "🛠️  Management commands:"
echo "  - Stop: ./scripts/stop.sh"
echo "  - Logs: ./scripts/logs.sh"
echo "  - Topics: ./scripts/topics.sh"
echo "  - Producer: ./scripts/producer.sh"
echo "  - Consumer: ./scripts/consumer.sh"
echo ""
echo "💡 KRaft Benefits:"
echo "  - No Zookeeper dependency"
echo "  - Faster startup time"
echo "  - Simplified architecture"
