from pymongo import Connection, ASCENDING
from django.conf import settings

def _get_url_cache():
    if not settings.CACHE_ENABLED:
        return
    connection = Connection(settings.MONGO_HOST, 27017)
    db = connection[settings.MONGO_DB_NAME]
    url_cache = db['url_cache']
    url_cache.ensure_index( [('url', ASCENDING)] )
    return url_cache

url_cache = _get_url_cache()


def _update_stats(hit):
    stats = url_cache.find_one({'_id': 'stats'})
    if stats is None:
        stats = { '_id': 'stats', 'req': 0, 'hits': 0 }
    stats['req'] += 1
    if hit:
        stats['hits'] += 1
    url_cache.insert(stats)


def get_stats():
    if not settings.CACHE_ENABLED:
        return (0,0)
    
    stats = url_cache.find_one({'_id': 'stats'})
    if stats is None:
        return (0, 0)
    return stats['req'], stats['hits']


def get_contents(url):
    if settings.CACHE_ENABLED:
        record = url_cache.find_one({'url': url})
        if record is None:
            _update_stats(False)
        else:
            _update_stats(True)
            return record['contents'], record['real_url']

    return None, None


def put_contents(url, contents, real_url):
    if not settings.CACHE_ENABLED:
        return
    try:
        url_cache.insert( {'url': url, 'contents': contents.encode('utf-8'), 'real_url': real_url } )
    except:
        print url
        print real_url
        print contents


def get_size():
    if not settings.CACHE_ENABLED:
        return 0
    return url_cache.count()


def clear(url):
    if settings.CACHE_ENABLED:
        url_cache.remove( {'url': url} )    
    

def empty():
    if settings.CACHE_ENABLED:
        url_cache.remove()
    