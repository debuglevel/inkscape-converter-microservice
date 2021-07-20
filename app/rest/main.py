#!/bin/usr/python3
import base64
import logging.config
import os
import tempfile
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.library import health
from app.rest.conversion import ConversionIn
from app.library import conversion

fastapi = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@fastapi.get("/health")
def get_health():
    logger.debug("Received GET request on /health")
    return health.get_health()


@fastapi.get("/health_async")
async def get_health_async():
    logger.debug("Received GET request on /health_async")
    return await health.get_health_async()


@fastapi.post("/images/")
async def convert_image(conversion_in: ConversionIn):
    logger.debug("Received POST request on /images/")

    with tempfile.NamedTemporaryFile(
        mode="wb", suffix=f".{conversion_in.inputformat}"
    ) as input_file:
        logger.debug("Decoding Base64 encoded input...")
        input_base64_bytes = conversion_in.base64.encode("ascii")
        input_bytes = base64.b64decode(input_base64_bytes)

        logger.debug(f"Writing input to '{input_file.name}'...")
        input_file.write(input_bytes)
        input_file.flush()
        input_size = os.path.getsize(input_file.name)
        logger.debug(f"Wrote input to '{input_file.name}': {input_size} bytes")

        # TODO: delete=False is a bad idea, because the file remains
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=f".{conversion_in.outputformat}", delete=False
        ) as output_file:
            conversion.convert(
                conversion_in.inputformat,
                conversion_in.outputformat,
                input_file,
                output_file,
            )

            logger.debug("Sending PDF file...")
            return FileResponse(
                output_file.name, filename=f"image.{conversion_in.outputformat}"
            )
