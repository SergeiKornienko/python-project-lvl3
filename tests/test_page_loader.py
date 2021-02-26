import requests_mock
from page_loader import download
import tempfile
from os import path
import pytest


@pytest.mark.parametrize(
    'path_input_file,path_expected_file,path_output_file,char,url',
    [
        ('tests/fixtures/index.html',
         'tests/fixtures/download_index.html',
         'ru-hexlet-io-courses.html',
         'r',
         'https://ru.hexlet.io/courses',
         ),
        ('tests/fixtures/nodejs.png',
         'tests/fixtures/nodejs.png',
         'ru-hexlet-io-courses_files/nodejs.png',
         'rb',
         'https://ru.hexlet.io/assets/professions/nodejs.png',
         ),
    ],
)
def test_download_file(
        path_input_file,
        path_expected_file,
        path_output_file,
        char,
        url):
    with open('tests/fixtures/index.html') as infile:
        html_input = infile.read()
    with open(path_input_file, char) as infile:
        file_input = infile.read()
    with open(path_expected_file, char) as infile:
        file_output = infile.read()
    with tempfile.TemporaryDirectory() as direct:
        with requests_mock.Mocker() as mock:
            mock.get('https://ru.hexlet.io/courses', text=html_input)
            if char == 'rb':
                mock.get(url, content=file_input)
            else:
                mock.get(url, text=file_input)
            download('https://ru.hexlet.io/courses', path_file=direct)
            with open(path.join(*(direct, path_output_file)), char) as infile:
                assert infile.read() == file_output
