import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

h = NullHandler()
logger = logging.getLogger("django_rds")
logger.addHandler(h)
