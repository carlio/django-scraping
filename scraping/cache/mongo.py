from pymongo import Connection, ASCENDING
from django.conf import settings
from scraping.cache.base import ScraperCacheBase
    
    
class MongoCache(ScraperCacheBase):

    def __init__(self):
        connection = Connection(settings.SCRAPER_CACHE_MONGO_HOST, 27017)
        db = connection[settings.SCRAPER_CACHE_MONGO_DB_NAME]
        url_cache = db['url_cache']
        url_cache.ensure_index( [('url', ASCENDING)] )
        self.url_cache = url_cache
    
    
    def _update_stats(self, hit):
        stats = self.url_cache.find_one({'_id': 'stats'})
        if stats is None:
            stats = { '_id': 'stats', 'req': 0, 'hits': 0 }
        stats['req'] += 1
        if hit:
            stats['hits'] += 1
        self.url_cache.insert(stats)
    
    
    def get_stats(self):
        stats = self.url_cache.find_one({'_id': 'stats'})
        if stats is None:
            return (0, 0)
        return stats['req'], stats['hits']
    
    
    def get_contents(self, url):
        record = self.url_cache.find_one({'url': url})
        if record is None:
            self._update_stats(False)
            return None, None
        else:
            self._update_stats(True)
            return record['contents'], record['real_url']
    
    
    def put_contents(self, url, contents, real_url):
        self.url_cache.insert( {'url': url, 'contents': contents.encode('utf-8'), 'real_url': real_url } )
    
    
    def get_size(self):
        return self.url_cache.count()
    
    
    def clear(self, url):
        self.url_cache.remove( {'url': url} )    
        
    
    def empty(self):
        self.url_cache.remove()
        