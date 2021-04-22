import os
import shutil
from urllib.parse import urljoin, urlsplit

import requests
from progress.bar import Bar

from page_loader.page_loader import module_logger
from page_loader.name_generator import create_file_name


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
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    # Set decode_content value to True
                    # otherwise the downloaded image file's size will be zero.
                    response.raw.decode_content = True
                else:
                    module_logger.error(
                        'Site {0}, res_url {1}\nCant download resource'.format(
                            url,
                            image_url,
                        ),
                    )

                    # Open a local file with wb ( write binary ) permission.
                with open(file_path, 'wb') as file:

                    shutil.copyfileobj(response.raw, file)
                    parent_dir_and_file = file_path.split('/')[-2:]
                    relative_path = os.path.join(*parent_dir_and_file)
                    imgtag['src'] = relative_path


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
                if not urlsplit(resource_url).netloc:
                    continue
                filename = create_file_name(resource_url)
                file_path = os.path.join(all_files_path, filename)

                response = requests.get(resource_url)
                if response.status_code != 200:
                    module_logger.error(
                        'Site {0}, res_url {1}\nCant download resource'.format(
                            url,
                            resource_url,
                        ),
                    )

                with open(file_path, 'wb') as file:

                    file.write(response.content)
                    parent_dir_and_file = file_path.split('/')[-2:]
                    relative_path = os.path.join(*parent_dir_and_file)
                    resource_tag[source_tags.get(resource_tag.name)] = relative_path
