from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix='/authentication',
    tags=['Authentication']
)


class RequestDTO(BaseModel):
    token: dict
    request: dict
