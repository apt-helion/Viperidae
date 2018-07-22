#!/usr/bin/env python

import base64

from aiohttp import web

from api.models import *

from api.modules.auth import authorise, refresh
from api.modules.error import error
from api.modules.search import Query
from api.modules.crawl import Spider
from api.modules.developer import DevQuery


async def test(request):
    return web.json_response({'status': 200, 'message': 'api.viperidae.api is up'})


async def index(request):
    """Indexes a site"""
    params = request.rel_url.query
    uri    = params.get('u')
    if not uri: return web.json_response(error(400))

    pages = await Spider(uri).crawl()
    return web.json_response(pages)


async def search(request):
    """Basic search function - site url & query"""
    params = request.rel_url.query
    uri    = params.get('u')
    query  = params.get('q')

    if not uri:   return web.json_response(error(400))
    if not query: return web.json_response(error(401))

    pages = await Spider(uri).crawl()

    return web.json_response(Query(pages, query).search())


async def auth(request):
    """Authenticate devs"""
    post = await request.post()

    auth_header   = request.headers.get('Authorization')
    head          = auth_header.split("Basic")[1]
    grant_type    = post.get('grant_type')
    refresh_token = post.get('refresh_token', '')

    client_id, client_secret = base64.b64decode(head).split(":")

    if not grant_type:    return web.json_response(error(430))
    if not client_id:     return web.json_response(error(450))
    if not client_secret: return web.json_response(error(451))

    if grant_type == 'authorization_code':
        return web.json_response(authorise(client_id, client_secret))

    if grant_type == 'refresh_token':
        return web.json_response(refresh_token(client_id, client_secret, refresh_token))

    return web.json_response(error(431))


async def dev_search(request):
    """Search function for devs - more features"""
    pass
