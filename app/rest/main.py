#!/bin/usr/python3
import base64
import logging.config
import os
import tempfile
import uuid

import aiofiles
from fastapi import FastAPI
from fastapi.openapi.models import Response
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


@fastapi.post(
    "/images/",
    # Specifying a response class that doesn't have a built-in media type
    # (Response, not JSONResponse) seems good enough to stop FastAPI from
    # from assuming that the response type is "application/json". Without
    # this, FastAPI adds "application/json" as a possible response even if
    # we manually set the `responses` attribute.
    response_class=FileResponse,
    responses={
        # Manually specify a possible response with our custom media type.
        200: {"content": {"application/octet-stream": {"schema": {"type": "string", "format": "binary"}}}}
    },
)
async def convert_image(conversion_in: ConversionIn):
    logger.debug("Received POST request on /images/")

    conversion_id = uuid.uuid4()

    async with aiofiles.tempfile.NamedTemporaryFile(
        mode="wb", suffix=f".{conversion_id}.{conversion_in.inputformat}"
    ) as input_file:
        logger.debug("Decoding Base64 encoded input...")
        input_base64_bytes = conversion_in.base64.encode("ascii")
        input_bytes = base64.b64decode(input_base64_bytes)

        logger.debug(f"Writing input to '{input_file.name}'...")
        await input_file.write(input_bytes)
        await input_file.flush()
        input_size = os.path.getsize(input_file.name)
        logger.debug(f"Wrote input to '{input_file.name}': {input_size} bytes")

        # TODO: delete=False is a bad idea, because the file remains
        async with aiofiles.tempfile.NamedTemporaryFile(
            mode="w", suffix=f".{conversion_id}.{conversion_in.outputformat}", delete=False
        ) as output_file:
            conversion.convert(
                conversion_in.inputformat,
                conversion_in.outputformat,
                input_file,
                output_file,
            )

            # CAVEAT: provide a random filename as some clients may write temporary files with this name
            # (and overwrite former files, which results in a great race condition)
            filename = f"{conversion_id}.{conversion_in.outputformat}"
            logger.debug(f"Sending PDF file as '{filename}' ...")
            return FileResponse(
                output_file.name, filename=filename
            )
