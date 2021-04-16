# -*- coding:utf-8 -*-

"""Module with tests for main function."""
import tempfile
import pytest
import os
import logging
import logging.config

from page_loader.page_loader import download
from bs4 import BeautifulSoup

# create logger
logger = logging.getLogger(__name__)


@pytest.mark.parametrize("url, right_name",

                         [
                             ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),
                             ('https://en.wikipedia.org/wiki/Lilith', 'en-wikipedia-org-wiki-Lilith.html'),
                             ('https://hexlettest.tiiny.site', 'hexlettest-tiiny-site.html'),
                         ])
def test_output(url, right_name):
    logging.info('!!!START!!!')
    with tempfile.TemporaryDirectory() as tempdir:
        name = download(url, tempdir)
        assert name == os.path.join(tempdir, right_name)
        # Check if image path changed to local. (must be true)
        with open(os.path.join(tempdir, name), 'r') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            for imgtag in soup.findAll('img'):
                assert imgtag.get('src').startswith(tempdir)

    logging.info('!!!FINISHED!!!')


@pytest.mark.parametrize("url",

                         ['https://site.com/404',
                          ])
def test_response_with_error(url):
    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(Exception):
            assert download(url, tmpdirname)
