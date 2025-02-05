from loguru import logger

from logging import config
from uvicorn.config import LOGGING_CONFIG

# Настраиваем формат логов uvicorn для запросов
LOGGING_CONFIG["formatters"]["access"]["fmt"] = (
    "%(asctime)s - %(levelname)s - %(client_addr)s - %(request_line)s - %(status_code)s"
)
LOGGING_CONFIG["formatters"]["access"]["datefmt"] = "%Y-%m-%d %H:%M:%S"

config.dictConfig(LOGGING_CONFIG)
