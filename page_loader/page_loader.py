from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from re import sub
from requests import request
from os import mkdir
from os.path import join, splitext


def download(url, dir_for_save=''):
    parsed_url_html = urlparse(url)
    (path_html, suffix_html) = splitext(parsed_url_html.path)
    name_html = get_name(parsed_url_html.netloc + path_html)
    path_for_save_html = join(dir_for_save, name_html + '.html')
    name_dir = name_html + '_files'
    path_for_save_files = join(dir_for_save, name_dir)
    mkdir(path_for_save_files)
    soup_from_html = BeautifulSoup(request('GET', url).text, 'html5lib')
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
                get_name(parsed_url_html.netloc + path_elem),
                suffix_elem,
            ])
            elem[attr] = join(name_dir, name_elem)
            file_elem = request('GET', urljoin(url, parsed_url_elem.path))
            if elem.name == 'img':
                decoding = 'wb'
                file_elem = file_elem.content
            else:
                decoding = 'w'
                file_elem = file_elem.text
            output_path_elem = join(path_for_save_files, name_elem)
            write_file(output_path_elem, file_elem, decoding)
    output_text_html = soup_from_html.decode(formatter="html5")
    write_file(path_for_save_html, output_text_html, 'w')
    return path_for_save_html


def write_file(path, content, decoding):
    with open(path, decoding) as infile:
        infile.write(content)


def is_current_domain(url_elem, url_html):
    domain_elem = urlparse(url_elem).netloc
    domain_html = urlparse(url_html).netloc
    return domain_elem == domain_html or domain_elem == ''


def get_name(path):
    return sub(r'[^a-zA-Z0-9]', '-', path)
