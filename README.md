django-scraping (ABANDONWARE)
=============================

*Note: I never got very far with this and none of this probably works any more.*

[![Build Status](https://secure.travis-ci.org/carlio/django-scraping.png)](http://travis-ci.org/carlio/django-scraping)

`django-scraping` is a library for making it easy to scrape content from websites.

Note: it is currently extremely alpha status in that it works for the specific use case that I use it for and probably not a lot else!


## Dependencies

Installing using `pip` will bring down most dependencies, but a few things require external packages to be installed.

### Required Dependencies

django-scraping relies upon PyQuery which in turn relies upon lxml. In order to
install lxml, you must have a compiler and development versions of python,
`libxml2` and `libxslt` available.

See also http://lxml.de/build.html


### Optional Dependencies

Some features require additional dependencies to be manually installed, because
the features are rarely used or because the dependency is "difficult" to install
(such as a dependency requiring native compilation against packages 

* For dealing with images, Pillow is required
  - see also http://pypi.python.org/pypi/Pillow#build-instructions-all-platforms

## Usage

This section is not too detailed for now because the API keeps changing as I figure out new use cases or problems with the existing definitions. As said: extremely alpha!

You will need to add `scraping` and `djcelery` to `INSTALLED_APPS` and run `syncdb` or `migrate`

Inside your django apps, create a `handlers.py`:

	# import the register function to add your handlers to django-scraping
    from scraping.handlers import register
    
    # define a callable
    def handle_something(doc, scraper_page):
        # doc is a pyquery document of the scraped content
        # scraper_page is the ScraperPage model, discussed below
        … do stuff with the doc …
    
    # map a name onto a callable
    register('handle_something', handle_something)
   
In the django admin, create a `ScraperPage` object, using 'handle_something' as the value for 'scraper'. In the `ScraperPage` list view, you can use an admin action to queue up a scrape.

Run `./manage.py celeryd` to execute the tasks. The `url` will be downloaded, parsed, and passed into your handler function.

More to come later..
