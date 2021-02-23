"""Function for launch cli-module."""
import argparse
import pathlib


def get_args():
    """Launch cli-module."""
    parser = argparse.ArgumentParser(description='download and save page')
    parser.add_argument('url', type=str)
    parser.add_argument(
        '-o', '--output',
        default=pathlib.Path(''),
        type=pathlib.Path,
        help='output dir (default: "/app")',
    )
    parser.add_argument(
        '-V', '--version', help='output the version number',
    )
    args = parser.parse_args()
    url = args.url
    path = args.output
    return url, path
