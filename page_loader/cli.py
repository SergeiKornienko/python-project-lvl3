"""Function for launch cli-module."""
import argparse
import pathlib
from os import getcwd


def get_args():
    """Launch cli-module."""
    parser = argparse.ArgumentParser(description='download and save page')
    parser.add_argument('url', type=str)
    parser.add_argument(
        '-o', '--output',
        default=getcwd(),
        type=pathlib.Path,
        help='output dir (default: "сurrent directory")',
    )
    args = parser.parse_args()
    url = args.url
    path = args.output
    return url, path
