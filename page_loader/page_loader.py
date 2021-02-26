from os import path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import requests


def get_name(url):
    parsed = urlparse(url)
    scheme = "%s://" % parsed.scheme
    name = parsed.geturl().replace(scheme, '', 1)
    return ''.join([re.sub(r'[^a-zA-Z0-9]', '-', name)])


def download(url, path_file=''):
    html_doc = requests.request('GET', url).text
    # soup = BeautifulSoup(html_doc, 'html5lib')
    # print(soup.prettify())
    # for src in soup.find_all('img'):

    name = path.join(*(path_file, ''.join([get_name(url), '.html'])))
    with open(name, 'w', encoding='utf-8') as infile:
        infile.write(html_doc)
    return name


if __name__ == '__main__':
    download('https://ru.hexlet.io/courses')



