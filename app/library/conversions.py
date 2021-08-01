import base64
import logging
import os
from pprint import pprint
from subprocess import call
import logging
import uuid
from typing import Optional, BinaryIO, List
from uuid import UUID

import aiofiles
from pydantic import BaseModel
from datetime import datetime
from tinydb import TinyDB, Query

from app.library import configuration

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

conversions: int = 0


class Conversion(BaseModel):
    id: Optional[str]
    input_format: str
    output_format: str
    created_on: Optional[str]


def get_conversions_directory():
    conversions_directory = configuration.get_configuration().conversions_directory
    os.makedirs(conversions_directory, exist_ok=True)
    return conversions_directory


def get_database_filename():
    database_directory = configuration.get_configuration().database_directory
    os.makedirs(database_directory, exist_ok=True)
    return f'{database_directory}/database.json'


def get_database():
    logger.debug(f"Opening TinyDB '{get_database_filename()}'...")
    database = TinyDB(get_database_filename())
    return database


async def add(conversion: Conversion) -> Conversion:
    logger.debug(f"Creating conversion...")

    conversion_id = str(uuid.uuid4()) # TODO test if str() is really needed

    conversion = conversion.dict() | {"id": conversion_id, "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    pprint(conversion)
    conversion = Conversion(**conversion)

    database = get_database()

    logger.debug(f"Inserting {conversion}...")
    document_id = database.insert(conversion.dict())

    logger.debug(f"Getting inserted...")
    retrieved_conversion_document = database.get(doc_id=document_id)
    logger.debug(f"Got inserted {retrieved_conversion_document}")

    logger.debug("Converting document to model...")
    retrieved_conversion = Conversion(**retrieved_conversion_document)
    logger.debug(f"Got inserted {retrieved_conversion}")

    return retrieved_conversion


async def get(id_: str) -> Conversion:
    logger.debug(f"Getting conversion with id={id_}...")

    database = get_database()

    conversion_query = Query()

    logger.debug(f"Getting document...")
    retrieved_conversion_document = database.get(conversion_query.id == id_)
    logger.debug(f"Got {retrieved_conversion_document}")

    logger.debug("Converting document to model...")
    retrieved_conversion = Conversion(**retrieved_conversion_document)
    logger.debug(f"Got {retrieved_conversion}")

    return retrieved_conversion


async def get_all() -> List[Conversion]:
    logger.debug(f"Getting conversions...")

    database = get_database()

    logger.debug(f"Getting document...")
    retrieved_conversion_documents = database.all()
    logger.debug(f"Got {retrieved_conversion_documents}")

    logger.debug("Converting documents to models...")
    retrieved_conversions = [Conversion(**retrieved_conversion_document) for retrieved_conversion_document in retrieved_conversion_documents]
    logger.debug(f"Got {retrieved_conversions}")

    return retrieved_conversions


async def delete(id_: str):
    logger.debug(f"Deleting conversion with id={id_}...")

    database = get_database()

    conversion_query = Query()

    logger.debug(f"Removing document...")
    database.remove(conversion_query.id == id_)


def get_filename_from_id(id_: str, output_format: str) -> str:
    logger.debug(f"Getting filename for output format={output_format}, id={id_}...")
    return f"{get_conversions_directory()}/{id_}.{output_format}"


async def save_input_file(conversion_: Conversion, base64_string: str):
    logger.debug(f"Saving input file for conversion id={conversion_.id}")
    filename = get_filename_from_id(conversion_.id, conversion_.input_format)

    async with aiofiles.open(file=filename, mode="wb") as input_file:
        logger.debug("Decoding Base64 encoded input...")
        base64_bytes = base64_string.encode("ascii")
        bytes_ = base64.b64decode(base64_bytes)

        logger.debug(f"Writing input to '{input_file.name}'...")
        await input_file.write(bytes_)
        await input_file.flush()
        size = os.path.getsize(input_file.name)
        logger.debug(f"Wrote input to '{input_file.name}': {size} bytes")


def convert(conversion: Conversion):
    logger.debug(f"Converting {conversion}...")

    input_file = get_filename_from_id(conversion.id, conversion.input_format)
    output_file = get_filename_from_id(conversion.id, conversion.output_format)

    convert_via_inkscape(conversion.input_format, conversion.output_format, input_file, output_file)


def convert_via_inkscape(input_format: str, output_format: str, input_filename: str, output_filename: str):
    logger.debug(
        f"Converting '{input_filename}' to '{output_filename}' via inkscape ({input_format} to {output_format})..."
    )

    global conversions
    conversions = conversions + 1

    process_arguments = [
        "inkscape",
        f"{input_filename}",
        f"--export-filename={output_filename}",
    ]
    logger.debug(f"Calling inkscape: {process_arguments}")
    call(process_arguments)
    logger.debug(f"Called inkscape")

    output_size = os.path.getsize(output_filename)
    logger.debug(f"Inkscape destination file '{output_filename}' has {output_size} bytes")
