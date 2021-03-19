import logging


def save(path, content):
    if isinstance(content, bytes):
        decoding = 'wb'
    else:
        decoding = 'w'
    with open(path, decoding) as infile:
        infile.write(content)
        logging.info('Save file: {a}'.format(a=path))
