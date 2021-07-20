from pydantic import BaseModel


class ConversionIn(BaseModel):
    base64: str
    inputformat: str
    outputformat: str
