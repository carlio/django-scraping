from django.conf import settings
from scraping.cache import cache
import requests
import celery
import logging
from celery.task.sets import subtask
import re
from celery.task import task



def fetch_url(url):
    user_agent = getattr(settings, 'SCRAPER_USER_AGENT', 'django-scraping v0.1')
    headers = { 'User-Agent': user_agent }
    
    resp = requests.get(url, headers=headers, timeout=30)
    return resp.text, resp.url


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