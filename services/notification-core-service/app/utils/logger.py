"""
Logging configuration and utilities

This module provides centralized logging setup and utilities for the notification
core service, including configurable log levels, formatting, and both console
and file output options.
"""

import logging
import sys
from typing import Optional

from ..config.settings import settings


def setup_logger(
    level: Optional[str] = None,
    format_string: Optional[str] = None,
    enable_file_logging: bool = False,
    log_file: str = "notification_service.log"
) -> logging.Logger:
    """Configure and initialize logging system
    
    Sets up the logging configuration with customizable levels, formats,
    and output destinations for the notification service.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom log format string
        enable_file_logging: Whether to log to file in addition to console
        log_file: Log file path
    
    Returns:
        Configured logger instance
    """
    
    # Use settings defaults if not provided
    level = level or settings.log_level
    format_string = format_string or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Create logger
    logger = logging.getLogger("notification_core_service")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        format_string,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if enable_file_logging:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Prevent duplicate logs
    logger.propagate = False
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(f"notification_core_service.{name}")
