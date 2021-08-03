import asyncio
import base64
import logging
import os
from subprocess import call

import aiofiles

from app.library import configuration, conversion_repository
from app.library.conversion_repository import Conversion

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

conversions: int = 0


def get_conversions_directory():
    logger.debug("Getting conversions directory...")
    conversions_directory = configuration.get_configuration().get_conversions_directory()

    if not os.path.isdir(conversions_directory):
        logger.debug(f"Conversion directory '{conversions_directory}' does not exist, creating directory...")
        os.makedirs(conversions_directory, exist_ok=True)

    return conversions_directory


def get_filename_from_id(id_: str, output_format: str) -> str:
    logger.debug(f"Getting filename for output format={output_format}, id={id_}...")
    return os.path.join(get_conversions_directory(), f"{id_}.{output_format}")


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


async def convert(conversion: Conversion):
    logger.debug(f"Converting {conversion}...")

    input_file = get_filename_from_id(conversion.id, conversion.input_format)
    output_file = get_filename_from_id(conversion.id, conversion.output_format)

    # start in new thread to not block the event loop
    await asyncio.to_thread(convert_via_inkscape, *(conversion.input_format, conversion.output_format, input_file, output_file))
    conversion.status = "done"

    await conversion_repository.update(conversion)


def convert_via_inkscape(
    input_format: str, output_format: str, input_filename: str, output_filename: str
):
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
    logger.debug(
        f"Inkscape destination file '{output_filename}' has {output_size} bytes"
    )
