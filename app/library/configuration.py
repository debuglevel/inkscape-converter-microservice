import logging
import os
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# TODO: it might be nice to incorporate dependency injection to override settings in testing:
#  https://fastapi.tiangolo.com/advanced/settings/#settings-and-testing
#  but that might also be possible without dependency injection.


@lru_cache()
def get_configuration():
    logger.debug("Getting configuration...")
    configuration = Configuration()
    logger.debug(f"Got configuration: {configuration}")
    return configuration


def ensure_directory_exists(path: str):
    logger.debug(f"Ensure configured directory {path} exists...")

    if not os.path.isdir(path):
        logger.warning(f"Configured directory '{path}' does not exist, creating directory...")
        os.makedirs(path, exist_ok=True)


class Configuration(BaseSettings):
    data_directory: str = "data/"
    database_directory: Optional[str]
    conversions_directory: Optional[str]

    def get_database_directory(self):
        if self.database_directory is None:
            directory = f"{self.data_directory}/database/"
            logger.debug(f"Database directory not specified. Using data directory: {directory}")
        else:
            directory = self.database_directory
            logger.debug(f"Database directory specified: {self.database_directory}")

        ensure_directory_exists(directory)
        return directory

    def get_conversions_directory(self):
        if self.conversions_directory is None:
            directory = f"{self.data_directory}/conversions/"
            logger.debug(f"Conversions directory not specified. Using data directory: {directory}")
        else:
            directory = self.conversions_directory
            logger.debug(f"Conversions directory specified: {directory}")

        ensure_directory_exists(directory)
        return directory

    class Config:
        env_file = "configuration.env"
