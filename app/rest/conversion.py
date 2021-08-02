from pydantic import BaseModel

from app.library.conversion_repository import Conversion


class ConversionRequest(BaseModel):
    base64: str
    inputFormat: str
    outputFormat: str


class ConversionResponse(BaseModel):
    id: str
    inputFormat: str
    outputFormat: str
    status: str
    createdOn: str
    modifiedOn: str


def to_conversion(conversion_request: ConversionRequest) -> Conversion:
    return Conversion(
        id=None,
        input_format=conversion_request.inputFormat,
        output_format=conversion_request.outputFormat,
        status="enqueued"
    )


def to_conversion_response(conversion_: Conversion) -> ConversionResponse:
    return ConversionResponse(
        id=conversion_.id,
        inputFormat=conversion_.input_format,
        outputFormat=conversion_.output_format,
        status=conversion_.status,
        createdOn=conversion_.created_on,
        modifiedOn=conversion_.modified_on,
    )
