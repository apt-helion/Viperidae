#!env/bin/python
import base64

from aiohttp import web

# from api.models import *

# from modules.auth import authorise
from api.modules.error import die
from api.modules.search import Query
from api.modules.crawl import Spider
# from modules.developer import DevQuery

async def test(request):
    return web.Response(text="api.viperidae.app is up")

async def index(request):
    """Index's a site"""
    params = request.rel_url.query
    uri    = params.get('u')
    if not uri:   return web.json_response(die(400))

    pages = await Spider(uri).crawl()
    return web.json_response(pages)

async def search(request):
    """Basic search function - site url & query"""
    params = request.rel_url.query

    uri   = params.get('u')
    query = params.get('q')

    if not uri:   return web.json_response(die(400))
    if not query: return web.json_response(die(401))

    pages = await Spider(uri).crawl()

    return web.json_response(Query(pages, query).search())

async def auth(request):
    """Authenticate devs"""
    auth_header = request.headers.get('Authorization')
    head        = auth_header.split("Basic")[1]

    client_id, client_secret = base64.b64decode(head).split(":")

    if not client_id:     return die(450)
    if not client_secret: return die(451)

    return authorise(client_id, client_secret)

def dev_search(request):
    """Search function for devs - more features"""
    pass


