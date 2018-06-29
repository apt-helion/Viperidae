#!/usr/bin/python3.6
from simplerr.web import web

from modules.auth import *
from modules.search import *
from modules.devSearch import *

from models import *

@web('/')
def index(request):
    pass

@web('/search', GET)
def search(request):
    """Basic search function - site url & query"""
    pass

@web('/auth', POST)
def auth(request):
    """Authenticate devs"""
    pass

@web('/devSearch', POST)
def dev_search(request):
    """Search function for devs - more features"""
    pass

