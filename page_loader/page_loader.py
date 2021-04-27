# -*- coding:utf-8 -*-

"""Module with main function."""
import os

import requests
from bs4 import BeautifulSoup

from page_loader.log_setup import logger
from page_loader.name_generator import create_html_name
from page_loader.resource_loader import download_local_res
from page_loader.storage import create_dir, write_html

module_logger = logger


def download(url, path):  # noqa: WPS210
    """Download web page to specific path.

    Args:
        url: str
        path: str

    Returns:
        Path to html file: str
    """
    file_name = create_html_name(url)
    file_path = os.path.join(path, file_name)

    response = requests.get(url)

    if response.status_code != 200:
        module_logger.error('Error with url {0}'.format(url))
        response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    dir_name = '{0}_files'.format(file_name[:-5])
    all_files_path = os.path.join(path, dir_name)
    create_dir(all_files_path)

    write_html(file_path, soup)

    # download_img(soup, all_files_path, url)
    download_local_res(soup, all_files_path, url)

    write_html(file_path, soup)

    return file_path
