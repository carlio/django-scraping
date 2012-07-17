from scraping.cache.base import ScraperCacheBase
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

try:
    import redis
except ImportError:
    raise ImproperlyConfigured('The "redis" python client package is required to use Redis as a cache - get it here http://pypi.python.org/pypi/redis/')

class RedisCache(ScraperCacheBase):
    
    def _get_db(self):
        info = { 'host': settings.SCRAPER_CACHE_REDIS_HOST,
                 'port': getattr(settings, 'SCRAPER_CACHE_REDIS_PORT', 6379),
                 'password': getattr(settings, 'SCRAPER_CACHE_REDIS_PASSWORD', None),
                 'db': settings.SCRAPER_CACHE_REDIS_DB }
        return redis.Redis(**info)

    def _key(self, url):
        return 'url:%s' % url 
    
    def _inc_req_count(self):
        self._get_db().incr('req')
    
    def _inc_hit_count(self):
        self._get_db().incr('hit')
    
    def get_stats(self):
        db = self._get_db()
        requests = int(db.get('req') or 0)
        hits = int(db.get('hit') or 0)
        return requests, hits
    
    
    def get_contents(self, url):
        self._inc_req_count()
        db = self._get_db()
        
        data = db.get(url)
        contents, real_url = data or (None, None)
        
        if contents is not None:
            self._inc_hit_count()
        return contents, real_url
    
    
    def put_contents(self, url, contents, real_url):
        db = self._get_db()
        db.set(url, (contents, real_url) )
    
    
    def get_size(self):
        return self._get_db().dbsize()
    
    def clear(self, url):
        self._get_db().delete(url)    
    
    def empty(self):
        self._get_db().flushdb()
    