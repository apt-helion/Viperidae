#!/usr/bin/env python

import asyncio
import json

from bson import json_util
from pymongo import MongoClient

from .search import Query
from .crawl import Spider


class ClientSpider(Spider):
    """
    Indexes the client website and saves all pages to a mongodb collection
    """

    def __init__(self, client):
        self.client = client
        uri = client.website

        super().__init__(uri)


    async def save_pages(self):
        """Save pages to mongodb"""
        pages = await self.crawl()

        mongo_client = MongoClient('localhost', 27017)
        database     = mongo_client.pages
        collection   = database[self.client.name]

        collection.delete_many({}) # delete previous pages
        collection.insert_many(pages) # insert new pages

        # Dump loaded BSON to valid JSON string and reload it as dict
        pages_sanitised = json.loads(json_util.dumps(pages))
        return pages_sanitised


class ClientQuery(Query):
    """
    Query a client
    """

    def __init__(self, client, query):
        self.client = client

        pages  = client.get_pages(client.name)
        query  = query

        super().__init__(pages, query)


    def modify_search(self):
        """Modify search with client settings"""
        pages = self.search()

        # Dump loaded BSON to valid JSON string and reload it as dict
        pages_sanitised = json.loads(json_util.dumps(pages))
        return pages_sanitised


if __name__ == "__main__":
    import doctest
    doctest.testmod()
