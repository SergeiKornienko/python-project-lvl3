from urllib.parse import ParseResult

import requests_mock
from page_loader import download
import tempfile
from os.path import join
from page_loader.html import prepare
import pytest
from requests import exceptions
from page_loader.url import is_local, parse


HTML = 'tests/fixtures/index.html'
NAME_HTML = 'ru-hexlet-io-courses.html'
EXPECT_HTML = 'tests/fixtures/download_index.html'
IMG = 'tests/fixtures/nodejs.png'
URL_IMG = 'https://ru.hexlet.io/assets/professions/nodejs.png'
PARSE_URL_IMG = ParseResult(
    scheme='',
    netloc='',
    path='/assets/professions/nodejs.png',
    params='',
    query='',
    fragment='',
)
URL = 'https://ru.hexlet.io/courses'
NAME_DIR = 'ru-hexlet-io-courses_files'
NAME_IMG = 'ru-hexlet-io-assets-professions-nodejs.png'
URL_JS = 'https://ru.hexlet.io/packs/js/runtime.js'
NAME_JS = "ru-hexlet-io-packs-js-runtime.js"
URL_CSS = 'https://ru.hexlet.io/assets/application.css'
NAME_CSS = "ru-hexlet-io-assets-application.css"
ASSETS = {
    join(NAME_DIR, NAME_CSS): URL_CSS,
    join(NAME_DIR, NAME_HTML): URL,
    join(NAME_DIR, NAME_IMG): URL_IMG,
    join(NAME_DIR, NAME_JS): URL_JS
}


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
        with open(join(direct, NAME_DIR, NAME_IMG), 'rb') as infile:
            assert infile.read() == img
        with open(join(direct, NAME_DIR, NAME_JS), 'r') as infile:
            assert infile.read() == 'test'
        with open(join(direct, NAME_DIR, NAME_CSS), 'r') as infile:
            assert infile.read() == 'test'
        assert path_html == join(direct, NAME_HTML)
        with open(path_html) as infile:
            assert infile.read() == html_expected


def test_prepare():
    with open(HTML) as infile:
        html_input = infile.read()
    with open(EXPECT_HTML) as infile:
        html_expected = infile.read()
    cooked_html, dict_assets = prepare(html_input, URL, NAME_DIR)
    assert cooked_html == html_expected
    assert dict_assets == ASSETS


def test_http():
    with pytest.raises(exceptions.RequestException):
        with requests_mock.Mocker() as mock:
            mock.get(URL, status_code=404)
            download(URL)


def test_os():
    with pytest.raises(OSError):
        with requests_mock.Mocker() as mock:
            mock.get(URL, text='test')
            download(URL, dir_for_save='/')


def test_is_local():
    assert is_local(URL_IMG, URL) is True
    assert is_local("https://cdn2.hexlet.io/assets/menu.css", URL) is False


def test_parse():
    assert parse(
        "/assets/professions/nodejs.png",
        'test',
        URL,
    ) == (NAME_IMG, PARSE_URL_IMG, join('test', NAME_IMG))
