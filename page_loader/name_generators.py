# -*- coding:utf-8 -*-


"""Module with generators for naming."""

import os
import re


def create_file_name(url):
    """Generate name for resource file, base on url.

    Args:
        url: str

    Returns:
        Name for image file.
    """
    file_name = delete_scheme(url)
    file_name = re.sub(r'[^\d.A-Za-z]|\.(?=[^/]+/)', '-', file_name)
    if len(file_name) > 40:
        file_name = file_name[-247:]
    if not os.path.splitext(file_name)[-1]:
        return '{0}.html'.format(file_name)
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


def create_relative_path(file_path):
    """Take parent directory and filename and return them.

    Args:
        file_path: str

    Returns:
        relative_path: str
    """
    parent_dir_and_file = file_path.split('/')[-2:]
    return os.path.join(*parent_dir_and_file)


def generate_file_path(all_files_path, resource_url):
    """Generate a path of resource file.

    Args:
        all_files_path: str
        resource_url: str

    Returns:
        full_path_to_file: str

    """
    filename = create_file_name(resource_url)
    return os.path.join(all_files_path, filename)
