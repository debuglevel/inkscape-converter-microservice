#!/bin/usr/python3
import asyncio
import base64
import logging.config
import os
import tempfile
import uuid
from pprint import pprint
from typing import List

from fastapi import FastAPI, status

import aiofiles
from fastapi import FastAPI
from fastapi.openapi.models import Response
from fastapi.responses import FileResponse
from app.library import health
from app.library.conversions import Conversion
from app.rest import conversion
from app.rest.conversion import ConversionRequest, ConversionResponse
from app.library import conversions
from fastapi import BackgroundTasks, FastAPI

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


@fastapi.get(
    "/images/{image_id}/download",  # Specifying a response class that doesn't have a built-in media type
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
async def download_image(image_id: str) -> FileResponse:
    logger.debug(f"Received GET request on /images/{image_id}/download")

    conversion_ = await conversions.get(image_id)
    filename = conversions.get_filename_from_id(conversion_.id, conversion_.output_format)

    # CAVEAT: provide a random filename as some clients may write temporary files with this name
    # (and overwrite former files, which results in a great race condition)
    filenamex = f"{conversion_.id}.{conversion_.output_format}"
    logger.debug(f"Sending file as '{filename}'...")
    return FileResponse(filename, filename=filenamex)


@fastapi.get("/images/{image_id}",
             response_model=ConversionResponse)
async def get_image(image_id: str) -> ConversionResponse:
    logger.debug(f"Received GET request on /images/{image_id}")

    conversion_ = await conversions.get(image_id)

    return conversion.to_conversion_response(conversion_)


async def save_and_convert(conversion_: Conversion, base64_string: str):
    await conversions.save_input_file(conversion_, base64_string)
    conversions.convert(conversion_)


@fastapi.post("/images/",
              status_code=status.HTTP_202_ACCEPTED,
              response_model=ConversionResponse)
async def post_image(conversion_request: ConversionRequest, background_tasks: BackgroundTasks) -> ConversionResponse:
    logger.debug("Received POST request on /images/")

    conversion_ = conversion.to_conversion(conversion_request)
    conversion_ = await conversions.add(conversion_)

    background_tasks.add_task(save_and_convert, *(conversion_, conversion_request.base64))

    return conversion.to_conversion_response(conversion_)


@fastapi.get("/images/",
             response_model=List[ConversionResponse])
async def get_images() -> List[ConversionResponse]:
    logger.debug(f"Received GET request on /images/")

    conversion_responses = [conversion.to_conversion_response(conversion_) for conversion_ in
                            await conversions.get_all()]
    return conversion_responses

# TODO: DELETE
