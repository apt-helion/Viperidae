#!env/bin/python
from aiohttp import web
from views import test, index, auth, search, dev_search

def setup_routes(app):
    app.router.add_get('/', test)
    app.router.add_get('/index', index)
    app.router.add_get('/search', search)
    app.router.add_post('/auth', auth)
    app.router.add_post('/devSearch', dev_search)

