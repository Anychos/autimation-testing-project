from pydantic import BaseModel


class ErrorDetailSchema(BaseModel):
    loc: list[str]
    msg: str
    type: str


class BaseErrorSchema(BaseModel):
    code: str
    message: str
    details: list[ErrorDetailSchema]


class HttpErrorSchema(BaseModel):
    error: BaseErrorSchema
