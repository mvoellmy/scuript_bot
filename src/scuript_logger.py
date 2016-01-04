import logging
import logging.config

logging.config.fileConfig('../cfg/logging.conf')

# create logger
logger = logging.getLogger('scuript_logger')

# 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')