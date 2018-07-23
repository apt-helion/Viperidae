#!/usr/bin/env python

import uuid

from .error import error
from ..models import *

from datetime import datetime


def authorise(client_id, client_secret):
    """Create an access token"""
    client = Clients.get(Clients.id == client_id, Clients.secret == client_secret)

    if not client: return error(410)

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
    client = Clients.get(Clients.id == client_id, Clients.secret == client_secret)

    if not client: return error(410)
    if not refresh_token: return error(405)

    previous_token = Tokens.get(Tokens.refresh_token == refresh_token)
    if not previous_token: return error(501)

    token  = uuid.uuid4().hex
    expiry = datetime.now() + datetime.timedelta(minutes = 30)

    Tokens.insert(
        client_id = client_id,
        token = token,
        refresh_token = '',
        expiry = expiry
    ).execute()

    previous_token.delete_instance()

    return {
        "access_token" : token,
        "token_type" : 'Bearer',
        "expires_in" : '1800'
    }


def get_token_client(token_id):
    """Checks if a token is valid and gets the client"""
    token = Tokens.get(Tokens.token == token_id)

    if not token: return error(411) # check token exists

    date = datetime.now() + datetime.timedelta(minutes = 30)
    if token.expiry > date: return error(550) # check token expiry

    return token.client
