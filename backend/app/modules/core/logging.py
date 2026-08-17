import logging
import os
from pythonjsonlogger import jsonlogger

from app.modules.core.config import settings

def setup_logging():
    logger = logging.getLogger()
    
    # # Clear existing handlers
    # if logger.hasHandlers():
    #     logger.handlers.clear()

    logHandler = logging.StreamHandler()
    
    # Ensure log directory exists
    log_path = settings.LOG_FILE_PATH
    log_dir = os.path.dirname(log_path)
    if log_dir and not os.path.exists(log_dir) and not os.environ.get("TESTING"):
        os.makedirs(log_dir, exist_ok=True)
    
    fileHandler = logging.FileHandler(log_path) if not os.environ.get("TESTING") else logging.NullHandler()
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    logHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.INFO)
