#!env/bin/python
from aiohttp import web
from views import test, index, auth, search, dev_search

def setup_routes(app):
    app.router.add_get('/', test)
    app.router.add_get('/index', index)
    app.router.add_get('/search', search)
    app.router.add_post('/v1/auth', auth)
    app.router.add_get('/v1/search', dev_search)
