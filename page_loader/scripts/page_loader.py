from page_loader.cli import get_args
from page_loader.page_loader import download
import sys
from requests import exceptions


def main():
    """Launch page_loader cli.

    Returns:
        Return cli.
    """
    try:
        print(download(*get_args()))
    except (OSError, exceptions.RequestException):
        sys.exit(1)


if __name__ == '__main__':
    main()
