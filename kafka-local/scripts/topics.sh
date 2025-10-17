#!/bin/bash

# Manage Kafka Topics
echo "📝 Kafka Topics Management..."

# Navigate to kafka-local directory
cd "$(dirname "$0")/.."

# Check if services are running
if ! docker-compose ps | grep -q "notification-hub-kafka.*Up"; then
    echo "❌ Kafka is not running. Please start it first with ./scripts/start.sh"
    exit 1
fi

case "${1:-list}" in
    "list")
        echo "📋 Listing all topics:"
        docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092
        ;;
    "create")
        if [ -z "$2" ]; then
            echo "❌ Please provide topic name: ./scripts/topics.sh create <topic-name>"
            exit 1
        fi
        echo "➕ Creating topic: $2"
        docker-compose exec kafka kafka-topics --create --topic "$2" --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
        ;;
    "delete")
        if [ -z "$2" ]; then
            echo "❌ Please provide topic name: ./scripts/topics.sh delete <topic-name>"
            exit 1
        fi
        echo "🗑️  Deleting topic: $2"
        docker-compose exec kafka kafka-topics --delete --topic "$2" --bootstrap-server localhost:9092
        ;;
    "describe")
        if [ -z "$2" ]; then
            echo "❌ Please provide topic name: ./scripts/topics.sh describe <topic-name>"
            exit 1
        fi
        echo "📊 Describing topic: $2"
        docker-compose exec kafka kafka-topics --describe --topic "$2" --bootstrap-server localhost:9092
        ;;
    *)
        echo "📝 Kafka Topics Management"
        echo ""
        echo "Usage: ./scripts/topics.sh <command> [topic-name]"
        echo ""
        echo "Commands:"
        echo "  list                    - List all topics"
        echo "  create <topic-name>     - Create a new topic"
        echo "  delete <topic-name>     - Delete a topic"
        echo "  describe <topic-name>   - Describe topic details"
        echo ""
        echo "Examples:"
        echo "  ./scripts/topics.sh list"
        echo "  ./scripts/topics.sh create my-topic"
        echo "  ./scripts/topics.sh describe notification-requests"
        ;;
esac
