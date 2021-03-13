from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from re import sub
from os.path import join, splitext


def cook(html, url, name_dir):
    soup_from_html = BeautifulSoup(html, 'html.parser')
    assets = {}
    for elem in soup_from_html.find_all(['img', 'script', 'link']):
        ref, attr = '', ''
        if elem.get('src'):
            ref = elem['src']
            attr = 'src'
        if elem.get('href'):
            ref = elem['href']
            attr = 'href'
        parsed_url_elem = urlparse(ref)
        (path_elem, suffix_elem) = splitext(parsed_url_elem.path)
        if is_current_domain(ref, url):
            name_elem = ''.join([
                get_name(urlparse(url).netloc + path_elem),
                suffix_elem,
            ])
            elem[attr] = join(name_dir, name_elem)
            assets[elem[attr]] = urljoin(url, parsed_url_elem.path)
    return soup_from_html.prettify(formatter="html"), assets


def is_current_domain(url_elem, url_html):
    domain_elem = urlparse(url_elem).netloc
    domain_html = urlparse(url_html).netloc
    return domain_elem == domain_html or domain_elem == ''


def get_name(path):
    return sub(r'[^a-zA-Z0-9]', '-', path)[:50]
