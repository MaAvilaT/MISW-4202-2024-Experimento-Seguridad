from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import constants
from models import LoggedUserRequest

router = APIRouter(
    prefix='/api/sportsman',
    tags=['Sportsman']
)


@router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if form_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication credentials were not provided'
        )

    response = requests.post(f'{constants.COMPONENT_AUTHENTICATION_BASE_URL}/authentication/token',
                             data={'username': form_data.username, 'password': form_data.password},
                             headers={'Content-Type': 'application/x-www-form-urlencoded'})

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=response.text)

    return response.json()


@router.post('/sync/sportsman')
async def synchronous_sportsman(request: LoggedUserRequest):

    response = requests.post(f'{constants.COMPONENT_AUTHENTICATION_BASE_URL}/authenticate', data=request.token)

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code,
                            detail=response.text)

    if response.user.role != 'SPORTSMAN':
        # TODO BLOCK USER, NOTIFY

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    response = requests.post(f'{constants.COMPONENT_AUTHORIZATION_BASE_URL}/authenticate', data=request.token)

    return response.json()
