"""Create logger for file and stderr."""
import logging
import os
from datetime import datetime
from functools import wraps


def call_counted(func):
    """Decorate to determine number of calls for a method.

    Args:
        func: function

    Returns:
        wrapper: decorator
    """

    @wraps(func)
    def wrapper(*args, **kwargs):  # noqa: WPS430
        wrapper.called += 1
        return func(*args, **kwargs)

    wrapper.called = 0
    return wrapper


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.warning = call_counted(logger.warning)
logger.error = call_counted(logger.error)
logger.critical = call_counted(logger.critical)

log_path = './logs'
try:
    os.mkdir(log_path)
except OSError:
    pass  # noqa: WPS420

date_time = datetime.now()
log_name = 'log{0}'.format(
    date_time.strftime('%d.%m.%Y %H:%M:%S'),
)  # noqa: WPS323, E501
log_console_formatter = logging.Formatter(
    '\n%(asctime)s [%(levelname)-5.5s]  %(message)s',
    '%d.%m.%Y %H:%M:%S',  # noqa: WPS323, E501
)

log_file_formatter = logging.Formatter(
    '%(asctime)s [%(levelname)-5.5s]  %(message)s\n',
    '%d.%m.%Y %H:%M:%S',  # noqa: WPS323, E501
)

file_handler = logging.FileHandler('{0}/{1}.log'.format(log_path, log_name))
file_handler.setFormatter(log_file_formatter)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_console_formatter)
console_handler.setLevel(logging.ERROR)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
