from django.utils.importlib import import_module
from django.conf import settings

cache_module = getattr(settings, 'SCRAPER_CACHE_MODULE', 'scraping.cache.dummy')
cache = import_module(cache_module)