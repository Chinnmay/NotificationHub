#!/bin/bash

# Show Kafka Local Environment Logs
echo "📋 Kafka Local Environment Logs..."

# Navigate to kafka-local directory
cd "$(dirname "$0")/.."

# Show logs for all services
docker-compose logs -f
