# -*- coding:utf-8 -*-

"""Module with argparse."""
import argparse


def take_args():
    """Pars arguments.

    Returns:
        arguments: any
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('path', default='', help='path to save file')
    parser.add_argument('url', type=str)
    return parser.parse_args()
