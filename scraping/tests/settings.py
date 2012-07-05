
INSTALLED_APPS = ['scraping', 'south']
try:
    import django_jenkins #@UnusedImport
except ImportError:
    pass
else:
    INSTALLED_APPS += ['django_jenkins']
    
PROJECT_APPS = ['scraping']

SCRAPER_CACHE_MODULE='scraping.cache.dummy'
SOUTH_TESTS_MIGRATE=False

DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
        }
}

