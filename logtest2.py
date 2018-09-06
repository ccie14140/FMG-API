#/usr/bin/python3

import syslog
import sys

syslog.openlog(address=("10.2.1.5","514"))

syslog.syslog(syslog.LOG_NOTICE, "a log notice - testing")
syslog.syslog(syslog.LOG_NOTICE, "Another log message: %s" % "Watch out!")

syslog.closelog()

