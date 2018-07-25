#!/usr/bin/env python

import uuid

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from api.models import *


def create():
    Client.create(
        client = uuid.uuid4().hex,
        secret = uuid.uuid4().hex,
        name = input('Enter name: '),
        website = input('Enter website: '),
        description = 'Test client please ignore.',
        user = 0
    )

    print('Client created...')


if __name__ == '__main__':
    create()
