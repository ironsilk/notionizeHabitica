import logging
from functools import wraps


def error_wrap(f):
    """
    Used to raise error HTTP error when request status != 200
    :param f:
    :return:
    """
    # print(f"Wrapped {f.__name__}", )

    @wraps(f)
    def wrap(*args, **kwargs):
        result = f(*args, **kwargs)
        if result.status_code != 200:
            result.raise_for_status()
        return result.json()

    return wrap


# Logger settings
def setup_logger(name, log_file=None, level=logging.INFO):
    """Function to setup as many loggers as you want"""
    formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} [%(name)s] [%(levelname)s] --> %(message)s')
    out_handler = logging.StreamHandler()
    out_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(out_handler)
    if log_file:
        handler = logging.FileHandler(log_file, encoding='utf8')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger