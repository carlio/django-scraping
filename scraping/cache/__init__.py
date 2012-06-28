from django.utils.importlib import import_module
from django.conf import settings

def _get_cache():
    cache_class = getattr(settings, 'SCRAPER_CACHE_CLASS', 'scraping.cache.dummy.DummyCache')
    module_name, class_name = cache_class.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, class_name)()



cache = _get_cache()