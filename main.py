#!/usr/bin/env python3
"""
NotificationHub - Main Application Entry Point

This is the primary entry point for the NotificationHub application,
which orchestrates the notification processing pipeline including
event consumption, transformation, and multi-channel delivery.
"""

from services.notification_core_service import app

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Notification Core Service...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
