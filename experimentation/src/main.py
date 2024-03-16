import logging
import subprocess

import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import random
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

API_GATEWAY_URL = 'http://localhost:7373'

VALID_SPORTSMAN_ENDPOINTS = [
    '/sportsman/recommendations',
    '/sportsman/profile',
    '/sportsman/events',
    '/sportsman/events/detail',
    '/sportsman/health',
]

INVALID_SPORTSMAN_ENDPOINTS = [
    '/org/list-sportsmen',
    '/org/profile',
    '/partner/events/list-sportsmen',
    '/partner/events',
    '/partner/profile',
]


def create_user(username, password, role='SPORTSMAN', email=''):
    email = email if email else f'{username}@gmail.com'

    user = {
        'username': username,
        'password': password,
        'role': role,
        'email': email,
    }
    response = requests.post(f'{API_GATEWAY_URL}/register', json=user)

    logger.log(logging.INFO, f'create user {user} response {response.json()}\n')

    return username, password, role, email, response.status_code, response.json()


def login_user(username, password):
    response = requests.post(f'{API_GATEWAY_URL}/api/sportsman/login',
                             data={'username': username, 'password': password},
                             headers={'Content-Type': 'application/x-www-form-urlencoded'})

    logger.log(logging.INFO, f'login user `{username}`, `{password}` response `{response.json()}`\n')

    return response.json().get('access_token'), response.json().get('token_type')


def execute_action(data, endpoint):
    time.sleep(0.05)

    response = requests.post(f'{API_GATEWAY_URL}/api/sportsman/sync/sportsman',
                             json={
                                 'token': {
                                     'access_token': data[-2],
                                     'token_type': data[-1],
                                 }, 'request': {
                                     'endpoint': endpoint
                                 }
                             })

    logger.log(logging.INFO, f'user `{data}`, `{endpoint}` executed action with response `{response.json()}`\n')

    return response.status_code, response.json()


def create_users_for_data_frame(number_of_users: int, common_name: str):
    created_users: list = []

    for idx in range(number_of_users):
        u, p, r, e, s, j = create_user(f'{common_name}_{idx}', f'password{idx}')
        time.sleep(0.05)
        a, t = login_user(u, p)
        time.sleep(0.05)
        created_users.append([u, p, r, e, s, j, a, t])

    return created_users


if __name__ == '__main__':
    logger.log(logging.INFO, f'Generating user requests')

    users = 10
    df = pd.DataFrame(create_users_for_data_frame(number_of_users=users, common_name='test_user'),
                      columns=['username', 'password', 'role', 'email', 'status_code', 'json_response',
                               'access_token', 'token_type'])

    logger.log(logging.INFO, f'creating spawns of `valid` requests to do actions')

    valid_requests_data: list = []
    valid_requests = np.random.randint(low=0, high=len(VALID_SPORTSMAN_ENDPOINTS), size=users * 10, dtype=np.int64)
    for i, df_row in zip(valid_requests, df.iloc[np.random.randint(low=0, high=len(df), size=users * 10)].values):
        status, response_json = execute_action(df_row, VALID_SPORTSMAN_ENDPOINTS[i])
        valid_requests_data.append([df_row[0], status, response_json, True])

    valid_requests_df = pd.DataFrame(valid_requests_data, columns=['username', 'status_code', 'response', 'invalid_user'])

    logger.log(logging.INFO, f'creating spawns of `invalid` requests to do actions')

    sample_size: int = int(len(df) * 0.1)  # take 10% of the users
    users_to_invalidate: list = random.sample([x for x in range(len(df))], sample_size)

    invalid_requests_data: list = []
    invalid_requests = np.random.randint(low=1, high=len(INVALID_SPORTSMAN_ENDPOINTS), size=sample_size, dtype=np.int64)
    for i, df_row in zip(invalid_requests, df.iloc[users_to_invalidate].values):
        status, response_json = execute_action(df_row, INVALID_SPORTSMAN_ENDPOINTS[i])
        invalid_requests_data.append([df_row[0], status, response_json, False])

    invalid_requests_df = pd.DataFrame(invalid_requests_data,
                                       columns=['username', 'status_code', 'response', 'invalid_user'])

    df.info(verbose=True)
    df.head()
    df.describe()

    df.head()
    valid_requests_df.info(verbose=True)
    valid_requests_df.describe()

    df.head()
    invalid_requests_df.info(verbose=True)
    invalid_requests_df.describe()

    subprocess.run(['bash', './stop_microservices.sh'])
