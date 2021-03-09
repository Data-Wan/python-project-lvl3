# -*- coding:utf-8 -*-

"""Module with UI."""
from page_loader.cli import take_args
from page_loader.page_loader import download

args = take_args()


def main():
    """Print generate diff for 2 json files."""

    print(download(args.url, args.path))


if __name__ == '__main__':
    main()
