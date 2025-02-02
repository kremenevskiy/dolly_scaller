import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from src.logger import logger


def load_env_file(fp: str) -> None:
    if not Path(fp).exists():
        raise FileNotFoundError(f"Environment file '{fp}' not found!")
    load_dotenv(fp, override=True)


load_env_file('.env')

env = os.getenv('ENV', 'test').lower()

if env == 'test':
    logger.info('Loaded test env')
    load_env_file('.env.test')

elif env == 'prod':
    logger.info('Loaded production env')
    load_env_file('.env.prod')
else:
    raise ValueError(f'Unknown environment: {env}')


@dataclass(frozen=True)
class DatabaseConf:
    host: str = os.environ['DB_HOST']
    db_name: str = os.environ['DB_NAME']
    db_user: str = os.environ['DB_USER']
    db_password: str = os.environ['DB_PASSWORD']
    db_port: int = int(os.environ['DB_PORT'])


class Config(BaseSettings):
    CORS_ORIGINS: list[str] = ['*']
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ['*']

    APP_VERSION: str = '0.1'


settings = Config()
