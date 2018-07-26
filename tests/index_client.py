#!/usr/bin/env python

import requests
import base64
import json
import pprint

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from data.models import *


def index_site(client):
    base64encoded = base64.b64encode(f'{client.client}:{client.secret}'.encode())
    header        = {'Authorisation': f'Bearer {base64encoded.decode()}'}

    print(f'\nIndexing {client.website}...')

    url           = 'http://0.0.0.0:8080/v1/index'
    get_request   = requests.get(url, headers=header)
    response_data = json.loads(get_request.text)

    print('\nIndexed Pages: ')
    for page in response_data:
        print(page['uri'])

    print('\nFinished')


def get_client():
    name = input('Enter client name: ')
    try:
        return Client.get(Client.name == name)
    except: sys.exit(f'Error: Could not find client "{name}"')


if __name__ == '__main__':
    index_site(get_client())
