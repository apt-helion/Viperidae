#!env/bin/python
import base64

from aiohttp import web

# from api.models import *

# from modules.auth import authorise
from api.modules.error import die
from api.modules.search import Query, Spider
# from modules.developer import DevQuery

async def index(request):
    params = request.rel_url.query
    return web.Response(text='Hello Aiohttp!')

async def search(request):
    """Basic search function - site url & query"""
    params = request.rel_url.query

    uri   = params.get('u')
    query = params.get('q')

    if not uri:   return die(400)
    if not query: return die(401)

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


