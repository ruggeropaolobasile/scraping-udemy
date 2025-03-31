import logging
import os
from datetime import datetime

# Directory dove salvare i log
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Nome file basato su data (opzionale)
log_filename = datetime.now().strftime("scraper_%Y-%m-%d.log")
log_path = os.path.join(LOG_DIR, log_filename)

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(log_path, encoding='utf-8'),
        logging.StreamHandler()  # Console
    ]
)

# Funzione utility per logging visivo

def log_section(title: str):
    border = "=" * 80
    logging.info(border)
    logging.info(f"== {title} ")
    logging.info(border)


def log_scraper(message: str):
    logging.info(f"[SCRAPER] {message}")


def log_warning(message: str):
    logging.warning(f"[SCRAPER-WARN] {message}")


def log_error(message: str):
    logging.error(f"[SCRAPER-ERR] {message}")


def log_debug(message: str):
    logging.debug(f"[SCRAPER-DEBUG] {message}")