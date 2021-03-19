from requests import request, exceptions
from os import mkdir
from os.path import join, splitext
from page_loader.html import prepare
from progress.bar import Bar
from page_loader.url import parse
from page_loader import storage
import logging
from urllib.parse import unquote


def download(url, dir_for_save='.'):

    name_file, parsed_url, path_to_file = parse(url, dir_for_save)
    name_dir = splitext(name_file)[0] + '_files'
    try:
        output_text_html, assets = prepare(get(url), url, name_dir)
        logging.info('List of assets:\n{a}'.format(a='\n'.join(assets)))
        storage.save(path_to_file, output_text_html)
        download_assets(assets, name_dir, dir_for_save)
        return path_to_file
    except exceptions.RequestException as error:
        logging.warning('Error request: {a}'.format(a=error))
        raise
    except OSError as error:
        logging.warning('Error writing of file: {a}'.format(a=error))
        raise


def get(url):
    r = request('GET', url)
    r.raise_for_status()
    return r.content


def download_assets(assets, name_dir, dir_for_save):
    try:
        if assets:
            make_dir(join(dir_for_save, name_dir))
    except OSError as error:
        logging.warning('Error writing of file: {a}'.format(a=error))
        raise
    for path_asset, url_asset in assets.items():
        with Bar(
                'Loading {asset}: '.format(asset=unquote(url_asset)),
                max=len(assets) / 100,
                suffix='%(percent)d%%') as bar_asset:
            try:
                content_asset = get(url_asset)
                storage.save(join(dir_for_save, path_asset), content_asset)
                bar_asset.next()
            except exceptions.RequestException as error:
                logging.warning('Error request: {a}'.format(a=error))
            except OSError as error:
                logging.warning('Error writing of file: {a}'.format(a=error))


def make_dir(path):
    try:
        mkdir(path)
        logging.info('Create directory for files: {a}'.format(a=path))
    except OSError as error:
        logging.warning('Error writing of file: {a}'.format(a=error))
