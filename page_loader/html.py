from urllib.parse import urljoin
from bs4 import BeautifulSoup
from page_loader.url import is_local, parse

TAGS = {
    'link': 'href',
    'script': 'src',
    'img': 'src',
}


def prepare(html, url_page, name_dir):
    soup_from_html = BeautifulSoup(html, 'html.parser')
    assets = {}
    for elem in soup_from_html.find_all(TAGS.keys()):
        tag = TAGS[elem.name]
        try:
            ref = elem[tag]
            if is_local(ref, url_page):
                name_file, parsed_url, path_to_file = parse(
                    ref,
                    name_dir,
                    url_page=url_page,
                )
                elem[tag] = path_to_file
                assets[elem[tag]] = urljoin(url_page, parsed_url.path)
        except KeyError:
            continue
    return soup_from_html.prettify(formatter="html5"), assets
