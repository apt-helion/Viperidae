#!/usr/bin/env python

from .search import Query


class ClientQuery(Query):
    """
    Query a client
    """

    def __init__(self, client, query):
        self.client = client
        self.pages  = client.get_pages()
        self.query  = query


if __name__ == "__main__":
    import doctest
    doctest.testmod()
