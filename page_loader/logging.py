import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('download.log', mode='w')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
formatter_ch = logging.Formatter(
    '%(levelname)s - %(message)s',
)
formatter_fh = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
fh.setFormatter(formatter_fh)
ch.setFormatter(formatter_ch)
logger.addHandler(fh)
logger.addHandler(ch)
