# -*- coding:utf-8 -*-

"""Module with main function."""

import requests
import re


def download(url, path):
    filename = delete_scheme(url)
    filename = re.sub('\W', '-', filename)
    filename = '{0}.html'.format(filename)
    file_path = '{0}/{1}'.format(path, filename)
    with open(file_path, 'w') as m:
        m.write(requests.get(url).text)
    return filename


def delete_scheme(url):
    if url.startswith('https://'):
        return url.replace('https://', '')
    else:
        return url.replace('http://', '')
