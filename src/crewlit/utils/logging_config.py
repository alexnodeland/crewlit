import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    root_logger.handlers.clear()

    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    colored_format = "┃ \033[1;33m%(asctime)s\033[0m ┃ \033[1;36m%(levelname)-8s\033[0m ┃ \033[1;32m%(name)-40s\033[0m ┃ \033[1;37m%(message)s\033[0m"
    date_format = "%Y-%m-%d %H:%M:%S"
    json_formatter = jsonlogger.JsonFormatter(log_format)
    standard_formatter = logging.Formatter(colored_format, datefmt=date_format)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(standard_formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(json_formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)

    # Set higher logging level for third-party libraries
    logging.getLogger("httpx").setLevel(logging.ERROR)
    logging.getLogger("asyncio").setLevel(logging.ERROR)
    logging.getLogger("openai").setLevel(logging.ERROR)
    logging.getLogger("httpcore").setLevel(logging.ERROR)
    logging.getLogger("charset_normalizer").setLevel(logging.ERROR)
    logging.getLogger("fsevents").setLevel(logging.ERROR)

def get_logger(name):
    return logging.getLogger(name)