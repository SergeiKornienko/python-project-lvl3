import requests_mock
from page_loader import download
import tempfile
from os import path


def test_download_file():
    with tempfile.TemporaryDirectory() as direct:
        with requests_mock.Mocker() as mock:
            mock.get('https://ru.hexlet.io/courses', text='data')
            download('https://ru.hexlet.io/courses', path_file=direct)
        with open(path.join(*(direct, 'ru-hexlet-io-courses.html'))) as infile:
            assert infile.read() == 'data'
