# -*- coding:utf-8 -*-

"""Module with UI."""
import logging
import sys

from page_loader import log_setup, page_loader  # noqa: F401
from page_loader.cli import take_args

args = take_args()

module_logger = logging.getLogger(__name__)


def main():
    """Download webpage."""
    module_logger.info('start downloading webpage')

    print(page_loader.download(args.url, args.output))

    module_logger.info('finished downloading')

    error_counter = log_setup.logger.error.called
    if error_counter:
        print(
            '{0} errors happened during download, check logs for more information'.format(error_counter),  # noqa: E501
        )
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
