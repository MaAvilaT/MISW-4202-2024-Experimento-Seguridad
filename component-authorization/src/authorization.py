from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix='/authorization',
    tags=['Authorization']
)


class RequestDTO(BaseModel):
    token: dict
    request: dict
