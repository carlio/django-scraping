
INSTALLED_APPS = ['scraping', 'south']

SCRAPER_CACHE_MODULE='scraping.cache.dummy'

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

