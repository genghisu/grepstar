import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        print str(record)

h = NullHandler()
logger = logging.getLogger("django_ec2")
#logger.addHandler(h)

