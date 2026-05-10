import logging
import os
from datetime import datetime

LOG_DIR = "reports/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name="test_logger"):
    log_file = os.path.join(
        LOG_DIR,
        f"run_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    )

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger