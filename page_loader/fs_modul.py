import os

from page_loader.page_loader import module_logger


def write_html(file_path, soup):
    with open(file_path, 'w', encoding='utf-8') as html_file:
        webpage_to_str = soup.prettify(formatter='html5')
        html_file.write(webpage_to_str)


def create_dir(all_files_path):
    try:
        os.mkdir(all_files_path)
    except OSError as error:
        module_logger.error(error)
