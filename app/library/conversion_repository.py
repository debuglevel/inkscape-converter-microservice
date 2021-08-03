import logging
import os
import uuid
from datetime import datetime
from typing import Optional, List

import aiofiles
from pydantic import BaseModel
from tinydb import TinyDB, Query

from app.library import configuration, conversions

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Conversion(BaseModel):
    id: Optional[str]
    input_format: str
    output_format: str
    status: str
    created_on: Optional[str]
    modified_on: Optional[str]


def get_database() -> TinyDB:
    logger.debug(f"Opening TinyDB '{get_database_filename()}'...")
    database = TinyDB(get_database_filename())
    return database


def get_database_filename() -> str:
    logger.debug("Getting database filename...")
    database_directory = configuration.get_configuration().get_database_directory()

    if not os.path.isdir(database_directory):
        logger.debug(f"Database directory '{database_directory}' does not exist, creating directory...")
        os.makedirs(database_directory, exist_ok=True)

    return os.path.join(database_directory, "database.json")


async def add(conversion: Conversion) -> Conversion:
    logger.debug(f"Adding...")

    conversion_id = str(uuid.uuid4())

    conversion = conversion.dict() | {
        "id": conversion_id,
        "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "modified_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    conversion = Conversion(**conversion)

    with get_database() as database:
        logger.debug(f"Inserting {conversion} in database...")
        document_id = database.insert(conversion.dict())
        logger.debug(f"Inserted {conversion} in database: doc_id={document_id}")

        logger.debug(f"Getting inserted with doc_id={document_id}......")
        retrieved_conversion_document = database.get(doc_id=document_id)
        logger.debug(f"Got inserted {retrieved_conversion_document}")

        logger.debug("Converting document to model...")
        retrieved_conversion = Conversion(**retrieved_conversion_document)
        logger.debug(f"Got inserted {retrieved_conversion}")

        return retrieved_conversion


async def update(conversion: Conversion) -> Conversion:
    logger.debug(f"Updating id={conversion.id}...")

    conversion = conversion.dict() | {
        "modified_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    conversion = Conversion(**conversion)

    with get_database() as database:
        conversion_query = Query()

        logger.debug(f"Updating {conversion} in database...")
        document_id = database.update(conversion.dict(), conversion_query.id == conversion.id)[0]
        logger.debug(f"Updated {conversion} in database: doc_id={document_id}")

        logger.debug(f"Getting updated with doc_id={document_id}...")
        retrieved_conversion_document = database.get(doc_id=document_id)
        logger.debug(f"Got updated {retrieved_conversion_document}")

        logger.debug("Converting document to model...")
        retrieved_conversion = Conversion(**retrieved_conversion_document)
        logger.debug(f"Got updated {retrieved_conversion}")

        return retrieved_conversion


async def get(id_: str) -> Conversion:
    logger.debug(f"Getting with id={id_}...")

    with get_database() as database:
        conversion_query = Query()

        logger.debug(f"Getting document...")
        retrieved_conversion_document = database.get(conversion_query.id == id_)
        logger.debug(f"Got {retrieved_conversion_document}")

        logger.debug("Converting document to model...")
        retrieved_conversion = Conversion(**retrieved_conversion_document)
        logger.debug(f"Got {retrieved_conversion}")

        return retrieved_conversion


async def get_all() -> List[Conversion]:
    logger.debug(f"Getting all...")

    with get_database() as database:
        logger.debug(f"Getting document...")
        retrieved_conversion_documents = database.all()
        logger.debug(f"Got {retrieved_conversion_documents}")

        logger.debug("Converting documents to models...")
        retrieved_conversions = [
            Conversion(**retrieved_conversion_document)
            for retrieved_conversion_document in retrieved_conversion_documents
        ]
        logger.debug(f"Got {retrieved_conversions}")

        logger.debug(f"Got {len(retrieved_conversions)} items...")
        return retrieved_conversions


async def delete_files(conversion_: Conversion):
    logger.debug(f"Deleting files for id={conversion_.id}...")

    for format_ in [conversion_.output_format, conversion_.input_format]:
        filename = conversions.get_filename_from_id(conversion_.id, format_)
        try:
            logger.debug(f"Deleting file '{filename}'...")
            await aiofiles.os.remove(filename)
        except OSError as e:
            logger.warning(f"Error while deleting file '{e.filename}': {e.strerror}")


async def delete(id_: str):
    logger.debug(f"Deleting with id={id_}...")

    conversion_ = await get(id_)
    await delete_files(conversion_)

    with get_database() as database:
        conversion_query = Query()

        logger.debug(f"Removing document...")
        database.remove(conversion_query.id == id_)
