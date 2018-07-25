#!/usr/bin/env python

import requests
import json
import pprint

from index_client import authenticate, get_client

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from data.models import *


def search_client(client):
    print(f'Authenticating {client.name}...')

    response = authenticate(client)

    query = input('\nEnter search query: ')

    url      = 'http://0.0.0.0:8080/v1/search'
    token    = response.get('access_token') # get access token
    header   = {'Authorization': f'Bearer {token}'}
    payload  = {'q': query}

    get_request   = requests.get(url, params=payload, headers=header)
    response_data = json.loads(get_request.text)

    for idx, page in enumerate(response_data):
        print('{}. Page: {}\nRank: {}\n'.format(idx, page['uri'], page['rank']))


if __name__ == '__main__':
    search_client(get_client())

