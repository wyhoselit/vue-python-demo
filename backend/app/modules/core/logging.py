import logging
from pythonjsonlogger import jsonlogger

from app.modules.core.config import settings

def setup_logging():
    logger = logging.getLogger()
    logHandler = logging.StreamHandler()
    fileHandler = logging.FileHandler(settings.LOG_FILE_PATH)
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    logHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.INFO)
