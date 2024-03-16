import os
from enum import Enum

COMPONENT_AUTHORIZATION_BASE_URL = os.environ.get('AUTHORIZATION_URL', 'http://localhost:4343')
COMPONENT_AUTHENTICATION_BASE_URL = os.environ.get('AUTHENTICATION_URL', 'http://localhost:9393')
COMPONENT_API_GATEWAY_BASE_URL = os.environ.get('API_GATEWAY_URL', 'http://localhost:7373')

LOGGER_NAME = 'com.psy.c.authorization'


class Role(Enum):
    SPORTSMAN = 'SPORTSMAN'
    ORG = 'ORG'
    BUSINESS_PARTNER = 'BUSINESS_PARTNER'
    SYSTEM_ADMIN = 'SYSTEM_ADMIN'


RULES: dict = {
    'SPORTSMAN': {
        '/sportsman/recommendations',
        '/sportsman/profile',
        '/sportsman/events',
        '/sportsman/events/detail',
        '/sportsman/health',
    },
    'ORG': {
        '/org/list-sportsmen',
        '/org/profile',
    },
    'BUSINESS_PARTNER': {
        '/partner/events/list-sportsmen',
        '/partner/events',
        '/partner/profile',
    },
    'SYSTEM_ADMIN': {
        '*',
    },
}
