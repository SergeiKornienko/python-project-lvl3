import requests_mock
from page_loader import download
import tempfile
from os import path
from bs4 import BeautifulSoup


HTML = 'tests/fixtures/index.html'
NAME_HTML = 'ru-hexlet-io-courses.html'
EXPECT_HTML = 'tests/fixtures/download_index.html'
IMG = 'tests/fixtures/nodejs.png'
URL_IMG = 'https://ru.hexlet.io/assets/professions/nodejs.png'
URL = 'https://ru.hexlet.io/courses'
NAME_DIR = 'ru-hexlet-io-courses_files'
NAME_IMG = 'ru-hexlet-io-assets-professions-nodejs.png'
URL_JS = 'https://ru.hexlet.io/packs/js/runtime.js'
NAME_JS = "ru-hexlet-io-packs-js-runtime.js"
URL_CSS = 'https://ru.hexlet.io/assets/application.css'
NAME_CSS = "ru-hexlet-io-assets-application.css"


def test_download_file():
    with open(HTML) as infile:
        html_input = infile.read()
    with open(EXPECT_HTML) as infile:
        html_expected = infile.read()
    with open(IMG, 'rb') as infile:
        img = infile.read()
    with tempfile.TemporaryDirectory() as direct:
        with requests_mock.Mocker() as mock:
            mock.get(URL, text=html_input)
            mock.get(URL_IMG, content=img)
            mock.get(URL_JS, text='test')
            mock.get(URL_CSS, text='test')
            path_html = download(URL, dir_for_save=direct)
        with open(path.join(direct, NAME_DIR, NAME_IMG), 'rb') as infile:
            assert infile.read() == img
        with open(path.join(direct, NAME_DIR, NAME_JS), 'r') as infile:
            assert infile.read() == 'test'
        with open(path.join(direct, NAME_DIR, NAME_CSS), 'r') as infile:
            assert infile.read() == 'test'
        assert path_html == path.join(direct, NAME_HTML)
        with open(path_html) as infile:
            assert BeautifulSoup(
                infile.read(),
                'html5lib',
            ) == BeautifulSoup(html_expected, 'html5lib')
