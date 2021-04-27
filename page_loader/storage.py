# -*- coding:utf-8 -*-

"""Module with fs manipulators."""

import os

from page_loader.log_setup import logger
from page_loader.name_generator import create_relative_path

module_logger = logger


def write_html(file_path, soup):
    """Prettify soup with html5 and write to file_path.

    Args:
        file_path: str
        soup: BS4
    """
    with open(file_path, 'w', encoding='utf-8') as html_file:
        webpage_to_str = soup.prettify(formatter='html5')
        html_file.write(webpage_to_str)


def create_dir(all_files_path):
    """Take all_files_path and try to create a directory.

    Args:
        all_files_path: str
    """
    try:
        os.mkdir(all_files_path)
    except OSError as error:
        module_logger.error(error)


def write_resource(file_path, resources, source_tag, response):
    """Write a resource to file_path.

    Args:
        file_path: str
        resources: dict
        source_tag: str
        response: binary

    Raises:
        OSError: If file not response.
    """
    try:
        with open(file_path, 'wb') as file:
            file.write(response.content)
            relative_path = create_relative_path(file_path)
            resources[source_tag] = relative_path
    except OSError as error:
        module_logger.error(error)
        raise
