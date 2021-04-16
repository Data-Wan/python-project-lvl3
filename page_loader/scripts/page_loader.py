# -*- coding:utf-8 -*-

"""Module with UI."""
import logging

from page_loader import log_setup, page_loader  # noqa: F401
from page_loader.cli import take_args

args = take_args()

module_logger = logging.getLogger(__name__)


def main():
    """Download webpage."""
    module_logger.info('start downloading webpage')
    print(page_loader.download(args.url, args.path))
    module_logger.info('finished downloading')


if __name__ == '__main__':
    main()
