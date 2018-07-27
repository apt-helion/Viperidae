#!/usr/bin/env python

import requests

from data.models import *

from .crawl import Spider
from .error import error

def send_head(uri):
    """Checks if uri exists"""
    try:
        p, h = Spider.get_protocol_hostname(uri)
        return True
    except: return False


def authorise(client_id, client_secret):
    """Check correct client_id client_secret"""
    client = Client.get(Client.client == client_id, Client.secret == client_secret)

    if not client: return False
    return client
