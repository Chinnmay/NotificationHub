"""
Utility modules for notification core service

This package provides common utility functions and helpers including
logging configuration, data validation, and shared functionality
used across the notification service components.
"""

from .logger import setup_logger, get_logger

__all__ = ['setup_logger', 'get_logger']
