# -*- coding:utf-8 -*-

"""Module with argparse."""
import argparse


def take_args():
    """Pars arguments.

    Returns:
        arguments: any
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='url to download')
    parser.add_argument('--output', '-o', default='./', help='path to save file (default: current)')  # noqa: E501
    return parser.parse_args()
