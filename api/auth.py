#!/usr/bin/env python

from .error import error
from data.models import *


def authorise(client_id, client_secret):
    """Check correct client_id client_secret"""
    client = Client.get(Client.client == client_id, Client.secret == client_secret)

    if not client: return False
    return client
