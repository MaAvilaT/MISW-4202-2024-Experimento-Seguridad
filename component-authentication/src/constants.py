import os

COMPONENT_AUTHORIZATION_BASE_URL = os.environ.get('AUTHORIZATION_URL', 'http://localhost:4343')
COMPONENT_AUTHENTICATION_BASE_URL = os.environ.get('AUTHENTICATION_URL', 'http://localhost:9393')
COMPONENT_API_GATEWAY_BASE_URL = os.environ.get('API_GATEWAY_URL', 'http://localhost:7373')


SECRET_KEY = os.environ.get('ENV_SECRET_KEY', 'TRD97kasj587TYFKG%$^&%HJB<8759YkasjdvmnJH<*O:YUIpoiLH>KJ')
ALGORITHM = os.environ.get('ENV_ALGORITHM', 'HS256')

TOKEN_VALIDITY_IN_MINUTES = 30
