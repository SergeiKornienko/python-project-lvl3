from os import path
from urllib.parse import urlparse
import re
import requests


def get_name(url):
    parsed = urlparse(url)
    scheme = "%s://" % parsed.scheme
    name = parsed.geturl().replace(scheme, '', 1)
    return ''.join([re.sub(r'[^a-zA-Z0-9]', '-', name), '.html'])


def download(url, path_file=''):
    t = requests.request('GET', url).text
    name = path.join(*(path_file, get_name(url)))
    with open(name, 'w', encoding='utf-8') as infile:
        infile.write(t)
    return name
