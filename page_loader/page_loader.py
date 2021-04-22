# -*- coding:utf-8 -*-

"""Module with main function."""
import os
import re

import requests
from bs4 import BeautifulSoup

from page_loader.fs_modul import write_html, create_dir
from page_loader.log_setup import logger
from page_loader.name_generator import delete_scheme
from page_loader.resource_loader import download_img, download_local_res

module_logger = logger


def download(url, path):  # noqa: WPS210
    """Download web page to specific path.

    Args:
        url: str
        path: str

    Returns:
        Path to html file: str

    Raises:
        Exception: if response is not 200
    """
    file_name = create_html_name(url)
    file_path = os.path.join(path, file_name)

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception

    soup = BeautifulSoup(response.text, 'html.parser')

    dir_name = '{0}_files'.format(file_name[:-5])
    all_files_path = os.path.join(path, dir_name)
    create_dir(all_files_path)

    write_html(file_path, soup)

    download_img(soup, all_files_path, url)
    download_local_res(soup, all_files_path, url)

    write_html(file_path, soup)

    return file_path


def create_html_name(url):
    """Generate name for html file, base on url.

    Args:
        url: str

    Returns:
        Name for html file.
    """
    file_name = delete_scheme(url)
    file_name = re.sub(r'\W', '-', file_name)
    return '{0}.html'.format(file_name)
