#!/usr/bin/env python

import os
import asyncio
import requests
import gc

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

class Spider():
    """
    Spider class used for crawl a website based of a provided seed uri.
    Used when website is not in db.

    Example usage:
    >>> uri     = 'https://blog.justinduch.com'
    >>> spider  = Spider(uri)
    >>> results = spider.crawl()
    >>> results # doctest +ELLPSIS
    [...]
    """

    cache = {}

    def __init__(self, uri, limit):
        self.uri      = uri
        self.limit    = limit
        self.hostname = urlparse(self.uri).netloc
        self.robots   = Spider.get_robots(self.hostname)

        self.loop = asyncio.get_event_loop()

        # initalise pages with seed link
        self.pages = [{
            'uri'     : self.uri,
            'links'   : self.get_links(self.uri),
            'content' : self.get_content(self.uri)
        }]

        self.crawled  = [self.uri] # uris that have been crawled


    @staticmethod
    def get_robots(host):
        robots      = []
        robots_file = os.popen(f'curl {host}/robots.txt').read()

        for line in robots_file.split("\n"):
            if line.startswith('Disallow'):
                robots.append(host+line.split(': ')[1].split(' ')[0])

        return robots


    @staticmethod
    def request_page(uri):
        """Gets the html for a page"""
        cache_key = hash(uri)
        if Spider.cache.get(cache_key): return Spider.cache[cache_key]

        page = requests.get(uri)
        html = BeautifulSoup(page.text, "html.parser")

        Spider.cache[cache_key] = html
        return html


    def check_url(self, uri):
        """Checks if the uri is a file or a webpage"""
        url   = urljoin(self.uri, uri) # join in case it's a relative link
        _file = False

        file_extentions = (
            '.jpg', '.png', '.gif', '.pdf', '.docx', '.webm',
            '.odt', '.doc', '.pptx', '.csv', '.xlsx', '.txt'
        )

        if '?' in url or '#' in url: return None
        if url.lower().endswith(file_extentions): _file = True
        if url.endswith('/'): url = url[:-1] # strip any trailing backslashes

        return { 'uri': url, 'file': _file }


    def get_content(self, uri):
        """Gets important text from a webpage"""
        html = self.request_page(uri)

        return {
            'title' : html.title.string,
            'text'  : html.get_text()
        }


    def get_links(self, uri):
        """Gets every link in a page"""
        html = self.request_page(uri)

        links = [self.check_url(a['href']) for a in html.find_all('a', href=True) if self.check_url(a['href'])]

        return links


    async def async_get_links(self, uri):
        """Gets every link in a page but asyncronously"""
        html = await self.loop.run_in_executor(ThreadPoolExecutor(), self.request_page, uri)

        links = [self.check_url(a['href']) for a in html.find_all('a', href=True) if self.check_url(a['href'])]

        return links


    async def handle_task(self, task_id, work_queue):
        """Handles the async work for crawling"""
        while not work_queue.empty():
            link = await work_queue.get()
            uri  = link['uri']

            if uri not in self.crawled and uri not in self.robots:
                self.crawled.append(uri)
                if self.hostname == urlparse(uri).netloc:

                    links = await self.async_get_links(uri)
                    for link in links:
                        if not link['file']: work_queue.put_nowait(link)

                    self.pages.append({
                        'uri'     : uri,
                        'links'   : links,
                        'content' : self.get_content(uri)
                    })

            if len(self.crawled) > self.limit: return


    async def crawl(self):
        """Sets the async queue, tasks, etc..."""
        queue = asyncio.Queue()

        [queue.put_nowait(link) for link in self.get_links(self.uri)]

        tasks = [self.handle_task(task_id, queue) for task_id in range(10)]

        await asyncio.wait(tasks)

        # I'm pretty sure Spider.cache causes a memory leak
        # so this just makes sure it is cleared, we don't need it anymore
        # I mean, I think it's a memory leak, I have no idea
        del(Spider.cache)
        gc.collect()
        Spider.cache = {}

        return self.pages


if __name__ == "__main__":
    import doctest
    doctest.testmod()
