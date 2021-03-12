from urllib.parse import urlparse
from requests import request, exceptions
from os import mkdir
from os.path import join, splitext
import logging
from page_loader.cooking_html import cook, get_name


def download(url, dir_for_save=''):
    logging.basicConfig(
        filename=join(dir_for_save, 'download.log'),
        filemode='w',
        level=logging.DEBUG,
    )
    parsed_url_html = urlparse(url)
    (path_html, suffix_html) = splitext(parsed_url_html.path)
    name_html = get_name(parsed_url_html.netloc + path_html)
    path_for_save_html = join(dir_for_save, name_html + '.html')
    name_dir = name_html + '_files'
    try:
        req = get(url)
        output_text_html, assets = cook(req.content, url, name_dir)
        logging.info('List of assets:\n{a}'.format(a='\n'.join(assets)))
        write_file(path_for_save_html, output_text_html)
        if assets:
            path_for_save_files = join(dir_for_save, name_dir)
            make_dir(path_for_save_files)
        download_assets(assets, dir_for_save)
        return path_for_save_html
    except exceptions.RequestException as error:
        logging.warning('Error request: {a}'.format(a=error))
        raise exceptions.RequestException
    except OSError as error:
        logging.warning('Error writting of file: {a}'.format(a=error))
        raise OSError


def write_file(path, content):
    if isinstance(content, bytes):
        decoding = 'wb'
    else:
        decoding = 'w'
    with open(path, decoding) as infile:
        infile.write(content)
        logging.info('Save file: {a}'.format(a=path))


def get(url):
    r = request('GET', url)
    r.raise_for_status()
    return r


def download_assets(assets, dir_for_save):
    for path_asset, url_asset in assets.items():
        try:
            req = get(url_asset)
            content_asset = req.content
            write_file(join(dir_for_save, path_asset), content_asset)
        except exceptions.RequestException as error:
            logging.warning('Error request: {a}'.format(a=error))
        except OSError as error:
            logging.warning('Error writting of file: {a}'.format(a=error))


def make_dir(path):
    try:
        mkdir(path)
        logging.info('Create directory for files: {a}'.format(a=path))
    except OSError as error:
        logging.warning('Error writting of file: {a}'.format(a=error))
