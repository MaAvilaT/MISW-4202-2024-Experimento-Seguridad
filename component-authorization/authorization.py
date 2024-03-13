from fastapi import APIRouter, Depends, HTTPException, status


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


class UserDTO(object):
    username: str

