# -*- coding:utf-8 -*-

"""Module with tests for main function."""
import tempfile
import pytest
import os

from page_loader.page_loader import download
from bs4 import BeautifulSoup


@pytest.mark.parametrize("url, right_name",

                         [
                             ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
                             ('https://en.wikipedia.org/wiki/Lilith', 'en-wikipedia-org-wiki-Lilith.html')

                         ])
def test_output(url, right_name):
    with tempfile.TemporaryDirectory() as tempdir:
        name = download(url, tempdir)
        assert name == right_name
        # Check if image path changed to local. (must be true) 
        with open(os.path.join(tempdir, name), 'r') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            for imgtag in soup.findAll('img'):
                assert imgtag['src'].startswith(tempdir)
