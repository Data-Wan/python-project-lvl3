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
