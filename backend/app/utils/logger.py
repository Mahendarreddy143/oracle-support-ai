"""Logging configuration"""

import logging
from app.config import settings


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    
    # Suppress noisy loggers
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
