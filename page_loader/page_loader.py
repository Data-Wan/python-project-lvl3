# -*- coding:utf-8 -*-

"""Module with main function."""

import os
import re

import requests


def download(url, path):
    """Download web page to specific path.

    Args:
        url: str
        path: str

    Returns:
        Path to html file: str
    """
    filename = delete_scheme(url)
    filename = re.sub(r'\W', '-', filename)
    filename = '{0}.html'.format(filename)
    file_path = os.path.join(path, filename)
    with open(file_path, 'w') as file:  # noqa: WPS110
        file.write(requests.get(url).text)
    return filename


def delete_scheme(url):
    """Delete a scheme of url.

    Args:
        url: str

    Returns:
        url without scheme: str
    """
    if url.startswith('https://'):
        return url.replace('https://', '')

    return url.replace('http://', '')
