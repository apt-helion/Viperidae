#!/usr/bin/python3.6

import re

class Query():
    """
    Query ranks pages it is given according to a query term

    Example usage:
    >>> uri = 'https://blog.justinduch.com'
    >>> spider = Spider(uri)
    >>> pages  = spider.crawl()
    >>> Query(pages, 'test').search()
    [...]
    """

    def __init__(self, pages, query):
        self.pages = pages
        self.query = query.lower()
        self.words = re.split(" ", self.query)

        self.ranked_pages = []

    def link_rank(self, page):
        """Adds to the rank of every page it points to"""
        for link in page['links']:
            uri = link['uri']
            for r_page in self.ranked_pages:
                if uri == r_page['uri']: r_page['l_rank'] += page['c_rank']

    def content_rank(self, page):
        """Gets a page and returns it with a rank based on content"""
        rank = 0

        for word in self.words:
            rank += len(re.findall(word, page['content']['title'].lower())) * 2
            rank += len(re.findall(word, page['content']['text'].lower()))

        page['c_rank'] = rank
        page['l_rank'] = 0 # initalise link rank

        return page

    def search(self):
        for page in self.pages:
            # Copy pages in to ranked_pages with ranks
            self.ranked_pages.append(self.content_rank(page))

        for page in self.ranked_pages:
            self.link_rank(page) # rank pages from links

        # Final pass to add ranks together
        for page in self.ranked_pages:
            page['rank'] = ((page['c_rank']*page['l_rank']) + page['l_rank']) / 2

        return sorted(self.ranked_pages, key=lambda k: k['rank'], reverse=True)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
