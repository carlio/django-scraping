from django.utils.importlib import import_module
from django.conf import settings

cache = import_module(settings.SCRAPER_CACHE_MODULE)