import requests_mock
from page_loader import download
import tempfile
from os import path
from bs4 import BeautifulSoup


def test_download_file():
    with open('tests/fixtures/index.html') as infile:
        html_input = infile.read()
    with open('tests/fixtures/download_index.html') as infile:
        html_expected = infile.read()
    with open('tests/fixtures/nodejs.png', 'rb') as infile:
        img = infile.read()
    with tempfile.TemporaryDirectory() as direct:
        with requests_mock.Mocker() as mock:
            mock.get('https://ru.hexlet.io/courses', text=html_input)
            mock.get(
                'https://ru.hexlet.io/assets/professions/nodejs.png',
                content=img,
            )
            download('https://ru.hexlet.io/courses', dir_for_save=direct)
        with open(path.join(
                direct,
                'ru-hexlet-io-courses_files',
                'ru-hexlet-io-assets-professions-nodejs.png',
        ),
                  'rb') as infile:
            assert infile.read() == img
        with open(path.join(*(direct, 'ru-hexlet-io-courses.html'))) as infile:
            assert BeautifulSoup(
                infile.read(),
                'html5lib',
            ) == BeautifulSoup(html_expected, 'html5lib')
