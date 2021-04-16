"""Create logger for file and stderr."""
import logging
import os
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

log_path = './logs'
try:
    os.mkdir(log_path)
except OSError:
    pass  # noqa: WPS420

date_time = datetime.now()
log_name = 'log{0}'.format(date_time.strftime('%d.%m.%Y %H:%M:%S'))  # noqa: WPS323, E501
log_formatter = logging.Formatter(
    '%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s',  # noqa: WPS323, E501
)


file_handler = logging.FileHandler('{0}/{1}.log'.format(log_path, log_name))
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.ERROR)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
