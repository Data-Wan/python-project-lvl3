# -*- coding:utf-8 -*-

"""Module with tests for main function."""
import tempfile
import pytest
import requests

from page_loader.page_loader import download


@pytest.mark.parametrize("url, right_name",

                         [
                             ('https://ru.hexlet.io/courses', 'ru-hexlet-io-courses.html'),

                         ])
def test_output(url, right_name):
    with tempfile.TemporaryDirectory() as tmpdir:
        name = download('https://ru.hexlet.io/courses', tmpdir)
        assert name == right_name
