# -*- coding: UTF-8 -*-
from celery.task import task
from celery.task.sets import subtask
from django.conf import settings
from pyquery import PyQuery as pq
import logging
import re
import urllib2
from scraping.cache import cache


def _open(url):
    headers = { 'User-Agent': settings.SCRAPER_USER_AGENT }
    req = urllib2.Request( url, headers=headers )
    resp = urllib2.urlopen( req, timeout=30 )
    
    content = resp.read()
    real_url = resp.geturl()
    
    if 'content-type' in resp.headers and 'charset=' in resp.headers['content-type']:
        content_type = resp.headers['content-type']
        encoding = content_type.split('charset=')[-1]
        content = unicode(content, encoding)
    elif 'http-equiv="content-type"' in content.lower() or 'http-equiv=\'content-type\'' in content.lower():
        # there is a meta tag declaring the encoding
        # <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
        matches = re.findall('charset=([a-zA-Z0-9-]+)', content)
        if len(matches) > 0:
            charset = matches[0]
            content = unicode(content, charset)
   
    return content, real_url
  

@task(rate_limit='1/s')
def fetch_html(url, callback):
  
    # get the XML and remove the namespace so we can use PyQuery (as
    # PyQuery fails when trying to use namespaces in selectors due to
    # an underlying lxml bug - see https://bitbucket.org/olauzanne/pyquery/issue/17/pyquery-fails-when-trying-to-query-a
    contents, real_url = _open(url)
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



    
def fetch(url, ffk, callback, callback_args=None, callback_kwargs=None):
    use_cache = ffk['use_cache']
    fetch_if_missing = ffk['fetch_if_missing']
    
    callback_args = callback_args or []
    callback_kwargs = callback_kwargs or {}
    
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
