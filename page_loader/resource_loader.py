# -*- coding:utf-8 -*-


"""Module with image and resources loader functions."""

from urllib.parse import urljoin, urlsplit

import requests
from progress.bar import Bar

from page_loader.fs_modul import write_resource
from page_loader.log_setup import logger
from page_loader.name_generators import generate_file_path

module_logger = logger


# def download_img(soup, all_files_path, url):  # noqa: WPS210
#     """Download image from web page to specific path.
#
#     Args:
#         soup: str
#         all_files_path: str
#         url: str
#
#     """
#     images = soup.findAll('img')
#     bar1 = Bar('Downloading images', suffix='%(percent)d%%')
#     for imgtag in images:
#         bar1.next()  # noqa: B305
#         source = imgtag.get('src')
#
#         image_url = urljoin(url, source)
#
#         file_path = generate_file_path(all_files_path, image_url)
#         response = requests.get(image_url, stream=True)
#         if response.status_code == 200:
#             # Set decode_content value to True
#             # otherwise the downloaded image file's size will be zero.
#             response.raw.decode_content = True
#         else:
#             module_logger.error(
#                 'Site {0}, res_url {1}\nCant download resource'.format(
#                     url,
#                     image_url,
#                 ),
#             )
#
#         write_image(file_path, imgtag, response)
#
#     bar1.finish()


def download_local_res(soup, all_files_path, url):  # noqa: WPS210, WPS231, C901
    """Download link and scripts from web page to specific path.

    Args:
        soup: str
        all_files_path: str
        url: str
    """
    res_dict = {'link': 'href', 'script': 'src', 'img': 'src'}
    for tag, source_tag in res_dict.items():
        download_source_tag(all_files_path, url, soup.findAll(tag), source_tag)


def download_source_tag(  # noqa: WPS231, WPS210, E501
    all_files_path,
    url,
    resources,
    source_tag,
):
    """Download source_tag from resources.

    Args:
        all_files_path: str
        url: str
        resources: list
        source_tag: str
    """
    bar1 = Bar('Downloading other resources', suffix='%(percent)d%%')
    for resource_tag in resources:
        bar1.next()  # noqa: B305
        source = resource_tag.get(source_tag)
        if (  # noqa: WPS337
            resource_tag.name != 'img'
            and (get_netloc(source) != get_netloc(url))
            and get_netloc(source)
        ):
            continue  # noqa: WPS220

        resource_url = urljoin(url, source)
        if not get_netloc(resource_url):
            continue
        file_path = generate_file_path(all_files_path, resource_url)

        response = requests.get(resource_url)
        if response.status_code != 200:
            module_logger.error(
                'Site {0}, res_url {1}\nCant download resource'.format(
                    url,
                    resource_url,
                ),
            )
        if resource_tag.name == 'img':
            response.raw.decode_content = True
        write_resource(file_path, resource_tag, source_tag, response)

    bar1.finish()


def get_netloc(url):
    """Return netloc from url.

    Args:
        url: str

    Returns:
        netloc: str
    """
    return urlsplit(url).netloc
