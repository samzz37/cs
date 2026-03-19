# Logging configuration

import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging():
    """Setup application logging"""
    
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # File handler
    fh = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    root_logger.addHandler(fh)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)
    
    return root_logger

# Initialize logger
logger = setup_logging()
