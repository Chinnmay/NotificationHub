#!/usr/bin/env python3
"""
End-to-End Integration Test Runner

This script executes comprehensive integration tests for the notification system,
validating the complete pipeline from event ingestion to notification delivery.
Requires Kafka and all notification services to be running.
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.e2e.test_simple_e2e import test_simple_e2e

def main():
    """Execute the end-to-end integration test suite"""
    print("🧪 Running End-to-End Integration Test...")
    print("📋 Prerequisites:")
    print("  ✅ Kafka running on localhost:9094")
    print("  ✅ Core Service running and processing events")
    print("  ✅ Channels Service running and processing notifications")
    print()
    
    try:
        asyncio.run(test_simple_e2e())
        print("\n🎉 E2E Test PASSED!")
        return 0
    except Exception as e:
        print(f"\n❌ E2E Test FAILED: {e}")
        return 1

if __name__ == "__main__":
    exit(main())