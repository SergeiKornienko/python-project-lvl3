from os.path import splitext
from urllib.parse import urlparse, unquote
from re import sub
from os.path import join


def is_local(url_elem, url_html):
    domain_elem = urlparse(url_elem).netloc
    domain_html = urlparse(url_html).netloc
    return domain_elem == domain_html or domain_elem == ''


def to_name(path):
    return sub(r'[^a-zA-Z0-9]', '-', unquote(path))


def parse(url, dir_for_save, url_page=None):
    parsed_url = urlparse(url)
    (path_file, suffix_file) = splitext(parsed_url.path)
    if suffix_file == '':
        suffix_file = '.html'
    netloc = urlparse(url_page).netloc if url_page else parsed_url.netloc
    name_file = ''.join([
        to_name(netloc + path_file),
        suffix_file,
        ])
    path_to_file = join(dir_for_save, name_file)
    return name_file, parsed_url, path_to_file
