import logging
from functools import lru_cache

from pydantic import BaseSettings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# TODO: it might be nice to incorporate dependency injection to override settings in testing:
#  https://fastapi.tiangolo.com/advanced/settings/#settings-and-testing
#  but that might also be possible without dependency injection.


@lru_cache()
def get_configuration():
    logger.debug("Getting configuration...")
    return Configuration()


class Configuration(BaseSettings):
    database_directory: str = "data/database/"
    conversions_directory: str = "data/conversions/"
    #some_string: str  # must be overridden by environment variable or startup fails
    #some_string_with_default: str = "Nyan Cat"
    #some_integer_with_default: int = 1138

    class Config:
        env_file = "configuration.env"
