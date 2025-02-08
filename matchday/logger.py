import logging
import json_log_formatter
import os

# Read log level from environment (default: DEBUG for development)
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

# Create a JSON log formatter
formatter = json_log_formatter.JSONFormatter()

# Create a file handler for structured logs
log_file = os.getenv("LOG_FILE", "logs.json")
file_handler = logging.FileHandler(filename=log_file) 
file_handler.setFormatter(formatter)

# Create a console handler (for local debugging)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Get the root logger and apply settings
logger = logging.getLogger()
logger.setLevel(getattr(logging, log_level, logging.DEBUG))
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Avoid duplicate logs from third-party libraries
logging.getLogger("openai").setLevel(logging.WARNING) 