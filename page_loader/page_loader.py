from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
import requests
import os
from os.path import join


def parse_url(url):
    dict_url = {}
    split_url = os.path.splitext(url)
    dict_url['url'] = os.path.split(url)[0]
    parsed_url = urlparse(split_url[0])
    dict_url['suffix'] = split_url[1]
    dict_url['netloc'] = re.sub(r'[^a-zA-Z0-9]', '-', parsed_url.netloc)
    dict_url['path'] = re.sub(r'[^a-zA-Z0-9]', '-', parsed_url.path)
    url_without_scheme_and_suffix = parsed_url.netloc + parsed_url.path
    dict_url['url_without_scheme_and_suffix'] = url_without_scheme_and_suffix
    dict_url['name_without_suffix'] = re.sub(
        r'[^a-zA-Z0-9]',
        '-',
        url_without_scheme_and_suffix,
    )
    return dict_url


def download(url, dir_for_save=''):
    text_html = requests.request('GET', url).text
    parsed_html_url = parse_url(url)
    path_dir_for_files = join(
        dir_for_save,
        (parsed_html_url['name_without_suffix'] + '_files'),
    )
    os.mkdir(path_dir_for_files)
    soup_from_html = BeautifulSoup(text_html, 'html5lib')
    for img in soup_from_html.find_all('img', src=re.compile('^[^h]')):
        parsed_img_url = parse_url(img['src'])
        file_img = requests.request(
            'GET',
            urljoin(url, img['src']),
        ).content
        img['src'] = join(
            (parsed_html_url['name_without_suffix'] + '_files'),
            ''.join(
                [parsed_html_url['netloc'],
                 parsed_img_url['path'],
                 parsed_img_url['suffix']],
            ),
        )
        with open(
                join(
                    path_dir_for_files,
                    ''.join(
                        [parsed_html_url['netloc'],
                         parsed_img_url['path'],
                         parsed_img_url['suffix']],
                    ),
                ),
                'wb') as infile:
            infile.write(file_img)
    with open(join(
            dir_for_save,
            (parsed_html_url['name_without_suffix'] + '.html'),
    ), 'w') as infile:
        infile.write(soup_from_html.decode(formatter="html5"))
    return dir_for_save + parsed_html_url['name_without_suffix'] + '.html'


# download('http://www.malero-guitare.fr/cours/gratte/')
# download('https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/bs4ru.html')
