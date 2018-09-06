import logging
import logging.handlers

log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = ('10.2.1.4',514))

formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)


def hello():
    my_message = input("Enter a string to test Syslog message: ")
    log.debug(my_message)
    log.critical('this is critical')

if __name__ == '__main__':
	hello()
