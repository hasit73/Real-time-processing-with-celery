import logging

LOG_FILE_PATH = "app.log"


def create_logger(logger_name):
    """Create a logger and returns logger object.

    Args:
        logger_name (str): Logger name

    Returns:
        logger: Logger Object.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # initialize file handler
    handler = logging.FileHandler(LOG_FILE_PATH, mode="w")
    # initialize log message formater
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
