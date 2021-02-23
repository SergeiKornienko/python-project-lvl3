from page_loader.cli import get_args
from page_loader.page_loader import download


def main():
    """Launch page_loader cli.

    Returns:
        Return cli.
    """
    return print(download(*get_args()))


if __name__ == '__main__':
    main()