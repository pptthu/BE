import logging
def setup_logging(level: str = "INFO"):
    level_val = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=level_val, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
