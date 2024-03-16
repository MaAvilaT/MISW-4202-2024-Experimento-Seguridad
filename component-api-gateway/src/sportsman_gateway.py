import logging
from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from . import constants
from .models import LoggedUserRequest

router = APIRouter(
    prefix='/api/sportsman',
    tags=['Sportsman']
)

logger = logging.getLogger(constants.LOGGER_NAME)


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Login for Sportsman.

    :param form_data: application/x-www-form-urlencoded form data with
    username and password only.

    :return: a JWT for authentication purposes with defined expiration.
    """
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


@router.post('/sync/sportsman', status_code=status.HTTP_200_OK)
async def synchronous_sportsman(request: LoggedUserRequest):
    """
    Synchronous api endpoint for authenticated Sportsmen.

    :param request: data that needs to comply with the `LoggedUserRequest` model.
    :return: the response from the synchronous action the sportsman is trying to achieve.
    """
    response = requests.get(f'{constants.COMPONENT_AUTHENTICATION_BASE_URL}/authenticate',
                            headers={'Content-Type': 'application/json',
                                     'Authorization': f'Bearer {request.token["access_token"]}'})

    if response.status_code != status.HTTP_200_OK:
        logger.log(level=logging.ERROR, msg=f'got response from `{constants.COMPONENT_AUTHENTICATION_BASE_URL}'
                                            f'/authenticate` but was `{response.json()}`')
        raise HTTPException(status_code=response.status_code,
                            detail='Unable to authenticate')

    if response.json().get('role') != 'SPORTSMAN':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    response = requests.post(f'{constants.COMPONENT_AUTHORIZATION_BASE_URL}/authorize', data=request.json())

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code,
                            detail='Unauthorized')

    # reach of this exercise, we would define logic here if this was a real app.

    return response.json()
