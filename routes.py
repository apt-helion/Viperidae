#!env/bin/python
from aiohttp import web
from views import test, index, search, dev_index, dev_search

def setup_routes(app):
    app.router.add_get('/', test)
    app.router.add_get('/index', index)
    app.router.add_get('/search', search)
    app.router.add_get('/v1/index', dev_index)
    app.router.add_get('/v1/search', dev_search)
