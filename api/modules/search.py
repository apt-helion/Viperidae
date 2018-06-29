#!/usr/bin/python3.6
import requests
import re

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

class Spider():
    """
    Spider class used for crawl a website based of a provided seed uri.
    Used when website is not in db.

    Example usage:
    >>> uri = 'https://blog.justinduch.com'
    >>> spider = Spider(uri)
    >>> spider.crawl()
    [...]
    """

    cache = {}

    def __init__(self, uri):
        self.uri = uri

    def cache_html(fn):
        def inner(uri):
            cache_key = hash(uri)
            if Spider.cache.get(cache_key): return Spider.cache[cache_key]

            Spider.cache[cache_key] = fn(uri)
            return Spider.cache[cache_key]

        return inner

    @staticmethod
    @cache_html
    def request_page(uri):
        """Gets the html for a page"""
        page  = requests.get(uri)
        html  = BeautifulSoup(page.text, "html.parser")

        return html

    def check_url(self, uri):
        """Checks if the uri is a file or a webpage"""
        url   = urljoin(self.uri, uri) # join in case it's a relative link
        _file = False

        file_extentions = (
            '.jpg', '.png', '.gif', '.pdf', '.docx',
            '.odt', '.doc', '.pptx', '.csv', '.xlsx'
        )

        if url.lower().endswith(file_extentions): _file = True
        if url.endswith('/'): url = url[:-1] # strip any trailing backslashes

        return { 'uri': url, 'file': _file }

    def get_content(self, uri):
        """Gets important text from a webpage"""
        html = self.request_page(uri)

        return html

    def get_links(self, uri):
        """Gets every link in a page"""
        html = self.request_page(uri)

        links = [self.check_url(a['href']) for a in html.find_all('a', href=True)]

        return links

    def crawl(self):
        """Gets all the pages in the website"""
        hostname = urlparse(self.uri).netloc

        # initalise pages with seed link
        pages = [{
            'uri'     : self.uri,
            'links'   : self.get_links(self.uri),
            'content' : self.get_content(self.uri)
        }]

        crawled  = []
        to_crawl = self.get_links(self.uri)

        while to_crawl:
            page = to_crawl.pop()
            uri  = page['uri']

            if not hostname == urlparse(uri).netloc: continue
            if uri in crawled: continue

            to_crawl += self.get_links(uri)
            pages.append({
                'uri'     : uri,
                'links'   : self.get_links(uri),
                'content' : self.get_content(uri)
            })

            crawled.append(uri)

        return pages

def Query():
    pass

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    uri = 'https://blog.justinduch.com'
    spider = Spider(uri)
    spider.crawl()
