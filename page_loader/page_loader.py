# -*- coding:utf-8 -*-

"""Module with main function."""
import os
import re
import shutil
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar

from page_loader.log_setup import logger

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
    try:
        os.mkdir(all_files_path)
    except OSError as error:
        module_logger.error(error)

    webpage_to_str = str(soup)

    with open(file_path, 'w', encoding='utf-8') as html_file:

        html_file.write(webpage_to_str)

    download_img(soup, all_files_path, url)
    download_local_res(soup, all_files_path, url)
    webpage_to_str = str(soup)
    with open(file_path, 'w', encoding='utf-8') as html_file1:
        html_file1.write(webpage_to_str)

    return file_name


def download_img(soup, all_files_path, url):  # noqa: WPS210
    """Download image from web page to specific path.

    Args:
        soup: str
        all_files_path: str
        url: str

    """
    images = soup.findAll('img')
    bar_length = len(images) if images else 1
    with Bar('Downloading images', max=bar_length) as bar1:
        for imgtag in images:
            bar1.next()  # noqa: B305
            source = imgtag.get('src')
            if source:
                image_url = urljoin(url, source)

                file_name = create_file_name(image_url)
                file_path = os.path.join(all_files_path, file_name)
                imgtag['src'] = file_path
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    # Set decode_content value to True
                    # otherwise the downloaded image file's size will be zero.
                    response.raw.decode_content = True
                else:
                    module_logger.error(
                        'Site {0}, res_url {1}\nCant download resource'.format(url, image_url),  # noqa: E501
                    )

                    # Open a local file with wb ( write binary ) permission.
                with open(file_path, 'wb') as file:  # noqa: WPS110

                    shutil.copyfileobj(response.raw, file)


def download_local_res(soup, all_files_path, url):  # noqa: WPS210, WPS231, C901
    """Download link and scripts from web page to specific path.

    Args:
        soup: str
        all_files_path: str
        url: str
    """
    resources = soup.findAll({'script': True, 'link': True})
    bar_length = len(resources) if resources else 1
    with Bar('Downloading other resources', max=bar_length) as bar1:
        for resource_tag in resources:
            bar1.next()  # noqa: B305
            source_tags = {'script': 'src', 'link': 'href'}

            source = resource_tag.get(source_tags.get(resource_tag.name))

            if source:
                if urlsplit(source).netloc:
                    if urlsplit(source).netloc != urlsplit(url).netloc:
                        continue  # noqa: WPS220
                resource_url = urljoin(url, source)
                if urlsplit(resource_url).netloc == '':
                    continue
                filename = create_file_name(resource_url)
                file_path = os.path.join(all_files_path, filename)

                resource_tag[source_tags.get(resource_tag.name)] = file_path

                response = requests.get(resource_url)
                if response.status_code != 200:
                    module_logger.error(
                        'Site {0}, res_url {1}\nCant download resource'.format(url, resource_url),  # noqa: E501
                    )

                with open(file_path, 'wb') as file:  # noqa: WPS110

                    file.write(response.content)


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


def create_file_name(url):
    """Generate name for resource file, base on url.

    Args:
        url: str

    Returns:
        Name for image file.
    """
    file_name = re.sub(r'[^\d.A-Za-z]|\.(?=[^/]+/)', '-', url)
    if len(file_name) > 40:
        file_name = file_name[-30:]
    return file_name


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
