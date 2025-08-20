import logging
import sys

def setup_logging(level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)
    # Clear handlers cũ
    for h in list(logger.handlers):
        logger.removeHandler(h)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
