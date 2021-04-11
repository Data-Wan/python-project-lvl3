# -*- coding:utf-8 -*-

"""Module with UI."""
import logging

from page_loader.cli import take_args
from page_loader.page_loader import download

args = take_args()


def main():
    """Print generate diff for 2 json files."""
    # Add logger
    logging.basicConfig(
        filename='debug.log',  # noqa: WPS317
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)',  # noqa: WPS323, E501
        datefmt='%Y-%m-%d %H:%M:%S',  # noqa: WPS323
    )
    logger = logging.getLogger(__name__)

    logger.info('start downloading webpage')
    print(download(args.url, args.path))
    logger.info('finished downloading')


if __name__ == '__main__':
    main()
