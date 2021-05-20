import sys
sys.path.append('../')
import logging
from src.config.settings import config

class LoggerService:
    def __init__(self):
       
        self.logger = logging.getLogger(config['LOGGING']['LOGGER'])
        self.logger.setLevel(logging.DEBUG)
        # define handlers
        handler = logging.StreamHandler() # handler para consola
        handler.setLevel(logging.DEBUG)
        logger_format = logging.Formatter(config['LOGGING']['FORMAT'])
        handler.setFormatter(logger_format)

        self.logger.addHandler(handler)

    def error(self, message):
        self.logger.error(message)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)

loggerService = LoggerService()

if __name__ ==  "__main__":
    # logger = LoggerService()
    loggerService.debug('This is a debug message')
    loggerService.info('This is an info message')
    loggerService.warning('This is a warning message')
    loggerService.error('This is an error message')
    loggerService.critical('This is a critical message')

