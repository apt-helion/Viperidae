#!env/bin/python
import uuid

from .error import error
from ..models import *

from datetime import datetime

def authorise(client_id, client_secret):
    """Create an access token"""
    client = Clients.get(Clients.id == client_id,
                         Clients.secret == client_secret)

    if not client: return error(500)

    token = uuid.uuid4().hex
    refresh_token = uuid.uuid4().hex
    expiry = datetime.now() + datetime.timedelta(minutes = 30)

    Tokens.insert(
        client_id = client_id,
        token = token,
        refresh_token = refresh_token,
        expiry = expiry
    ).execute()

    return {
        "access_token" : token,
        "token_type" : 'Bearer',
        "expires_in" : '1800',
        "refresh_token" : refresh_token
    }

def refresh(client_id, client_secret, refresh_token):
    """Refresh access token - only one refresh allowed"""
    client = Clients.get(Clients.id == client_id,
                         Clients.secret == client_secret)

    if not client: return error(500)
    if not refresh_token: return error(600)

    previous_token = Tokens.get(Tokens.refresh_token == refresh_token)
    if not previous_token: return error(601)

    token = uuid.uuid4().hex
    expiry = datetime.now() + datetime.timedelta(minutes = 30)

    Tokens.insert(
        client_id = client_id,
        token = '',
        refresh_token = refresh_token,
        expiry = expiry
    ).execute()

    previous_token.delete_instance()

    return {
        "access_token" : token,
        "token_type" : 'Bearer',
        "expires_in" : '1800'
    }

