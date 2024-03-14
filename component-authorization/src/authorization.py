from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel


router = APIRouter(
    prefix='/authentication',
    tags=['Authentication']
)

RULES: dict = {
    'SPORTSMAN': {
        '/authentication',
    },
    'ORG': {
        '/authentication',
    },
    'BUSINESS_PARTNER': {
        '/authentication',
    },
    'SYSTEM_ADMIN': {
        '*',
    },
}


class UserDTO(BaseModel):
    username: str
    password: str

