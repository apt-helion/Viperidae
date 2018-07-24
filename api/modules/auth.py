#!/usr/bin/env python

import uuid

from .error import error
from ..models import *

from datetime import datetime, timedelta


def authorise(client_id, client_secret):
    """Create an access token"""
    client = Client.get(Client.client == client_id, Client.secret == client_secret)

    if not client: return error(410)

    token = uuid.uuid4().hex
    refresh_token = uuid.uuid4().hex
    expiry = datetime.now() + timedelta(minutes = 30)

    Token.insert(
        token = token,
        refresh_token = refresh_token,
        expiry = expiry,
        client_id = client_id
    ).execute()

    return {
        "access_token" : token,
        "token_type" : 'Bearer',
        "expires_in" : '1800',
        "refresh_token" : refresh_token
    }


def refresh(client_id, client_secret, refresh_token):
    """Refresh access token - only one refresh allowed"""
    client = Client.get(Client.client == client_id, Client.secret == client_secret)

    if not client: return error(410)
    if not refresh_token: return error(405)

    previous_token = Tokens.get(Token.refresh_token == refresh_token)
    if not previous_token: return error(501)

    token  = uuid.uuid4().hex
    expiry = datetime.now() + timedelta(minutes = 30)

    Token.insert(
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
    token = Token.get(Token.token == token_id)

    if not token: return error(411) # check token exists

    date = datetime.now() + timedelta(minutes = 30)
    if token.expiry > date: return error(550) # check token expiry

    return token.client
