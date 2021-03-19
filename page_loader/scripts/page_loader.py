from page_loader.cli import get_args
from page_loader.page_loader import download
import sys
from requests import exceptions
from page_loader.log import setup


def main():
    """Launch page_loader cli.

    Returns:
        Return cli.
    """
    url, path, log = get_args()
    setup(loglevel=log)
    try:
        print(download(url, path))
    except (OSError, exceptions.RequestException):
        sys.exit(1)


if __name__ == '__main__':
    main()
