import logging

LOGLEVEL = {
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG
        }


def setup(loglevel=0):
    """Set up logging to file and console."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
        filename='./download.log',
        filemode='w',
    )
    console = logging.StreamHandler()
    console.setLevel(LOGLEVEL[loglevel])
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
