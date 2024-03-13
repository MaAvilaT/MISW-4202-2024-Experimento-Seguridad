import os

COMPONENT_AUTHORIZATION_BASE_URL = os.environ.get('AUTHORIZATION_URL', 'http://localhost:4343')
COMPONENT_AUTHENTICATION_BASE_URL = os.environ.get('AUTHENTICATION_URL', 'http://localhost:8080')
COMPONENT_API_GATEWAY_BASE_URL = os.environ.get('API_GATEWAY_URL', 'http://localhost:7373')

