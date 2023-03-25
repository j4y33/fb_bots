import logging
from config.config import config

logging.basicConfig(filename=config.filename, format=config.format, level=config.level)
logger = logging.getLogger('selenium_log')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)