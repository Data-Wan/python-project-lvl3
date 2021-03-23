# -*- coding:utf-8 -*-

"""Module with main function."""

import os
import re
import shutil
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup


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

    soup = BeautifulSoup(response.text, 'html.parser')

    with open(file_path, 'w+', encoding='utf-8') as html_file:
        webpage_to_str = str(soup)
        html_file.write(webpage_to_str)
        download_img(soup, path, file_name, url)
        html_file.truncate(0)
        webpage_to_str = str(soup)
        html_file.write(webpage_to_str)

    return file_name


def download_img(soup, path, html_name, url):  # noqa: WPS210
    """Download image from web page to specific path.

    Args:
        soup: str
        path: str
        html_name: str
        url: str

    """
    dir_name = '{0}_files'.format(html_name[:-5])
    all_imgs_path = os.path.join(path, dir_name)
    os.mkdir(all_imgs_path)

    for imgtag in soup.findAll('img'):
        source = imgtag['src']

        if source.startswith('//'):
            image_url = 'http:{0}'.format(delete_scheme(source))
        else:
            template_url = '{0.scheme}://{0.netloc}{1}'
            image_url = template_url.format(urlsplit(url), source)

        file_name = create_image_name(image_url)
        file_path = os.path.join(all_imgs_path, file_name)
        imgtag['src'] = file_path
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            # Set decode_content value to True
            # otherwise the downloaded image file's size will be zero.
            response.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(file_path, 'wb') as file:  # noqa: WPS110

            shutil.copyfileobj(response.raw, file)


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


def create_image_name(url):
    """Generate name for image file, base on url.

    Args:
        url: str

    Returns:
        Name for image file.
    """
    return re.sub(r'\W(?!jpg|png|PNG|JPG)', '-', url)


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
