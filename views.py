#!/usr/bin/env python

import base64

from aiohttp import web

from data.models import *

from api.error import error
from api.modules import send_head, authorise

from api.search import Query
from api.crawl import Spider
from api.developer import ClientSpider, ClientQuery


routes = web.RouteTableDef()

@routes.get('/')
async def test(request):
    return web.json_response({'status': 200, 'message': 'api.viperidae.app is up'})

##########################
# API for public viewing #
##########################

@routes.get('/index')
async def index(request):
    """Indexes a site"""
    params = request.rel_url.query
    uri    = params.get('u')

    if not uri:            return web.json_response(error(400))
    if not send_head(uri): return web.json_response(error(411))

    pages = await Spider(uri, 50).crawl()
    return web.json_response(pages)


@routes.get('/search')
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

@routes.get('/v1/index')
async def dev_index(request):
    """Indexes a site"""
    try:
        auth_header = request.headers["Authorisation"]
        head        = auth_header.split("Bearer ")[1]
    except KeyError:   return web.json_response(error(503))
    except IndexError: return web.json_response(error(502))

    b64decoded = base64.b64decode(head).decode()
    client_id, client_secret = b64decoded.split(":")

    client = authorise(client_id, client_secret)
    if not client: return web.json_response(error(410))

    pages = await ClientSpider(client).save_pages()
    return web.json_response(pages)


@routes.get('/v1/search')
async def dev_search(request):
    """Search function for clients - uses client settings"""
    try:
        auth_header = request.headers["Authorisation"]
        head        = auth_header.split("Bearer ")[1]
    except KeyError:   return web.json_response(error(503))
    except IndexError: return web.json_response(error(502))

    b64decoded = base64.b64decode(head).decode()
    client_id, client_secret = b64decoded.split(":")

    client = authorise(client_id, client_secret)
    if not client: return web.json_response(error(410))

    params = request.rel_url.query
    query  = params.get('q')

    if not query: return web.json_response(error(401))

    return web.json_response(ClientQuery(client, query).modify_search())


# Setup Routes
def setup_routes(app):
    app.router.add_routes(routes)
