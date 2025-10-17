#!/bin/bash

# Stop Kafka Local Environment
echo "🛑 Stopping Kafka Local Environment..."

# Navigate to kafka-local directory
cd "$(dirname "$0")/.."

# Stop services
docker-compose down

echo "✅ Kafka Local Environment stopped!"
echo ""
echo "💡 To completely clean up (remove volumes):"
echo "   docker-compose down -v"
