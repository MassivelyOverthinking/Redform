
#########################################################################################################
# IMPORTS
#########################################################################################################

import logging
import logging.config
import os

from pathlib import Path

#########################################################################################################
# LOGGER CONFIGURATION
#########################################################################################################

# Configure the Global Logging setup.
def configure_logging() -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    Path("logs").mkdir(exist_ok=True)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": log_level,
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "level": log_level,
                    "formatter": "default",
                    "filename": "logs/app.log",
                    "encoding": "utf-8",
                },
            },
            "root": {
                "level": log_level,
                "handlers": ["console", "file"],
            },
        }
    )

# Create and retrieve a package native Logger-instance.
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name=name)