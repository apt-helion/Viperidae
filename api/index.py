#!/usr/bin/python3.6
import base64

from simplerr.web import web
from models import *

from modules.auth import authorise
from modules.error import die

from modules.search import Query, Spider
from modules.developer import DevQuery

@web('/')
def index(request):
    pass

@web('/search', GET)
def search(request):
    """Basic search function - site url & query"""
    uri   = request.args.get('u')
    query = request.args.get('q')

    if not uri:   return die(400)
    if not query: return die(401)

    pages = Spider(uri).crawl()
    if 'error' in pages: die(pages['status'])

    return Query(pages, query).search()

@web('/authorize', POST)
def auth(request):
    """Authenticate devs"""
    auth_header = request.headers.get('Authorization')
    head        = auth_header.split("Basic")[1]

    client_id, client_secret = base64.b64decode(head).split(":")

    if not client_id:     return die(450)
    if not client_secret: return die(451)

    return authorise(client_id, client_secret)

@web('/devSearch', POST)
def dev_search(request):
    """Search function for devs - more features"""
    pass

