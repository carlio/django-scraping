

class ScraperCacheBase(object):

    """
    Base class to define the methods that are expected of a cache.
    """
    # I kind of miss Java interfaces here...

    def get_stats(self):
        raise NotImplementedError
    
    def get_html(self, url):
        raise NotImplementedError

    def put_html(self, url, html, real_url):
        raise NotImplementedError
    
    def get_size(self):
        raise NotImplementedError

    def clear(self, url):
        raise NotImplementedError
    
    def empty(self):
        raise NotImplementedError
