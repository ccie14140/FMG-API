import logging
import logging.handlers

logger = logging.getLogger('FROM-API')
logger.setLevel(logging.DEBUG)

#add handler to the logger
handler = logging.handlers.SysLogHandler('/dev/log')

#add formatter to the handler
formatter = logging.Formatter('%(asctime)s %(name)-8s %(message)s')

handler.formatter = formatter
logger.addHandler(handler)

logger.debug("Test Message-logtest4-from-api.py")