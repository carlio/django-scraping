from scraping.cache.base import ScraperCacheBase

class DummyCache(ScraperCacheBase):

    """
    No-op version of the cache for testing
    """

    def get_stats(self):
        return 0, 0
    
    def get_html(self, url):
        return None

    def put_html(self, url, html, real_url):
        pass
    
    def get_size(self):
        return 0

    def clear(self, url):
        pass
    
    def empty(self):
        pass
