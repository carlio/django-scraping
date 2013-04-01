
INSTALLED_APPS = ['scraping']

SECRET_KEY='django-scraping-tests-settings'

for module in ('django_jenkins', 'south'):
    try:
        __import__(module)
    except ImportError:
        pass
    else:
        INSTALLED_APPS += [module]
    
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

