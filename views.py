#!/usr/bin/env python

import base64

from aiohttp import web

from api.models import *

from api.modules.error import error
from api.modules.auth import authorise, refresh, get_token_client

from api.modules.search import Query
from api.modules.crawl import Spider
from api.modules.developer import ClientQuery


async def test(request):
    return web.json_response({'status': 200, 'message': 'api.viperidae.app is up'})

##########################
# API for public viewing #
##########################

async def index(request):
    """Indexes a site"""
    params = request.rel_url.query
    uri    = params.get('u')
    if not uri: return web.json_response(error(400))

    pages = await Spider(uri, 50).crawl()
    return web.json_response(pages)


async def search(request):
    """Basic search function - site url & query"""
    params = request.rel_url.query
    uri    = params.get('u')
    query  = params.get('q')

    if not uri:   return web.json_response(error(400))
    if not query: return web.json_response(error(401))

    pages = await Spider(uri, 50).crawl()

    return web.json_response(Query(pages, query).search())

###################
# API for clients #
###################

async def auth(request):
    """Authenticate devs"""
    post = await request.post()

    try:
        auth_header = request.headers["Authorization"]
        head        = auth_header.split("Basic ")[1]
    except KeyError:   return web.json_response(error(503))
    except IndexError: return web.json_response(error(502))

    grant_type    = post.get('grant_type')
    refresh_token = post.get('refresh_token', '')

    client_id, client_secret = base64.b64decode(head).split(":")

    if not grant_type:    return web.json_response(error(402))
    if not client_id:     return web.json_response(error(404))
    if not client_secret: return web.json_response(error(405))

    if grant_type == 'authorization_code':
        return web.json_response(authorise(client_id, client_secret))

    if grant_type == 'refresh_token':
        return web.json_response(refresh_token(client_id, client_secret, refresh_token))

    return web.json_response(error(500))


async def dev_search(request):
    """Search function for clients - uses client settings"""
    try:
        auth_header = request.headers["Authorization"]
        head        = auth_header.split("Bearer ")[1]
    except KeyError:   return web.json_response(error(503))
    except IndexError: return web.json_response(error(502))

    token = head[0]
    if not token: return web.json_response(error(403))

    client = get_token_client(token)
    if 'error' in client: return client # client is an error message

    params = request.rel_url.query
    query  = params.get('q')

    if not query: return web.json_response(error(401))

    return web.json_response(ClientQuery(client, query).search())
