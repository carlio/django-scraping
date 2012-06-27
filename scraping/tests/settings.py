
INSTALLED_APPS = ['django_jenkins', 'scraping', 'south']
PROJECT_APPS = ['scraping']

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

