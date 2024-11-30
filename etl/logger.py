import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_file="etl_pipeline.log", max_bytes=5_000_000, backup_count=3):
    """
    Set up a logger for the ETL pipeline with both file and console handlers.

    Parameters:
    - log_file: Name of the log file to store logs.
    - max_bytes: Maximum size (in bytes) before rotating the log file.
    - backup_count: Number of backup log files to retain.

    Returns:
    - A configured logger instance.
    """
    logger = logging.getLogger("ETL_Pipeline")
    logger.setLevel(logging.DEBUG)  # Log everything (DEBUG and above)

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setLevel(logging.DEBUG)  # Capture detailed logs in the file

    # Console handler for real-time feedback
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Show higher-level logs in the console

    # Common log format
    log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Initialize the logger
logger = setup_logger()
