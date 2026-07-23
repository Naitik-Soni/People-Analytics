"""Logger module for logging important parts of the application"""
from loguru import logger

logger.remove()

logger.add(
    "logs/app.log",
    level="INFO",
    rotation="100 MB",
    retention="30 days",
)