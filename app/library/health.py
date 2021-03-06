import logging
from datetime import datetime

from pydantic import BaseModel

from app.library.conversions import conversions

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Health(BaseModel):
    status: str
    datetime: datetime


def get_health() -> Health:
    logger.debug("Getting health...")
    health: Health = Health(
        status="up", datetime=datetime.now(), conversions=conversions
    )
    return health


async def get_health_async() -> Health:
    logger.debug("Getting health (async)...")
    health: Health = Health(
        status="up", datetime=datetime.now(), conversions=conversions
    )
    return health
