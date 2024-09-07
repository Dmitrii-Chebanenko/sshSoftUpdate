import logging


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.getLogger('paramiko').setLevel(logging.CRITICAL)

    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
