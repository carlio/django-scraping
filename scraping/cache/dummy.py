from scraping.cache.base import ScraperCacheBase

class DummyCache(ScraperCacheBase):

    """
    No-op version of the cache for testing
    """

    def get_stats(self):
        return 0, 0
    
    def get_contents(self, url):
        return None, None

    def put_contents(self, url, contents, real_url):
        pass
    
    def get_size(self):
        return 0

    def clear(self, url):
        pass
    
    def empty(self):
        pass
