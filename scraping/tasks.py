# -*- coding: UTF-8 -*-
from celery.task import task, periodic_task
from celery.task.sets import subtask
from datetime import timedelta
from pyquery import PyQuery as pq
from scraping.cache import cache
from scraping.handlers import registry
from scraping.ioutils import fetch_url
from scraping.models import PeriodicScrape, PageType, ScrapeStatus
import celery
import feedparser
import logging
import re
import traceback




@periodic_task(run_every=timedelta(seconds=5))
def scrape_indexes():
    # TODO: could this be more efficient by selecting periodic scrapes by filtering
    # the most recent scrape attempt? 
    # see http://blog.roseman.org.uk/2010/08/14/getting-related-item-aggregate/
    # but it doesn't look nice...
    
    for scraper_page in PeriodicScrape.objects.filter(enabled=True):
        if scraper_page.scrape_due():
            # we need to scrape!
            scraper_page.schedule_scrape()
              
        
@task
def handle_page_scrape(contents, url, ffk, scraper_page, attempt):
    if scraper_page.page_type == PageType.HTML:
        doc = make_doc(contents, url)
    elif scraper_page.page_type == PageType.RSS:
        doc = feedparser.parse(contents)
    else:
        attempt.complete(state=ScrapeStatus.FAILURE, error_message="Unknown page type: %s" % scraper_page.page_type)
        raise NotImplementedError
    
    try:
        registry[scraper_page.scraper](doc, scraper_page)
    except Exception:
        error_message = traceback.format_exc()
        attempt.complete(ScrapeStatus.FAILURE, error_message)
    else:
        attempt.complete()


@task(rate_limit='1/s')
def fetch_html(url, callback):
  
    # get the XML and remove the namespace so we can use PyQuery (as
    # PyQuery fails when trying to use namespaces in selectors due to
    # an underlying lxml bug - see https://bitbucket.org/olauzanne/pyquery/issue/17/pyquery-fails-when-trying-to-query-a
    contents, real_url = fetch_url(url)
    contents = re.sub('xmlns.*?".*?"','',contents)
    
    # stick the contents into the cache
    cache.put_html(url, contents, real_url)
    
    # TODO: in celery 2.6, this is unecessary - see http://ask.github.com/celery/whatsnew-2.6.html#group-chord-chain-are-now-subtasks
    subtask(callback).delay(contents, real_url)
    
    
def make_doc(html, url):
    # create a pq object
    d = pq(html)
    d.make_links_absolute(base_url=url)
    return d



    
def fetch(url, ffk, callback_or_taskname, callback_args=None, callback_kwargs=None):
    use_cache = ffk['use_cache']
    fetch_if_missing = ffk['fetch_if_missing']
    
    callback_args = callback_args or []
    callback_kwargs = callback_kwargs or {}
    
    if isinstance(callback_or_taskname, (str, unicode)):
        callback = celery.registry.tasks[callback_or_taskname]
    else:
        callback = callback_or_taskname
    
    if use_cache:
        html, real_url = cache.get_html(url)
        
    logging.debug('cache %s for %s' % ('hit' if html is not None else 'miss', url))
        
    if (html is None and fetch_if_missing) or not use_cache:
        args = [ffk] + callback_args
        fetch_html.delay(url, callback=callback.subtask(args=args, kwargs=callback_kwargs))
    else:
        args = [html, real_url, ffk] + callback_args
        callback.delay(*args, **callback_kwargs )


def get_ffk(use_cache=True, fetch_if_missing=True):
    return {'use_cache': use_cache,
            'fetch_if_missing': fetch_if_missing }
    
    

