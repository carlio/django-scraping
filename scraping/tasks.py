# -*- coding: UTF-8 -*-
from celery.task import task, periodic_task
from datetime import timedelta
from pyquery import PyQuery as pq
from scraping.handlers import registry
from scraping.models import PeriodicScrape, PageType, ScrapeStatus
import feedparser
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
        doc = pq(contents)
        doc.make_links_absolute(base_url=url)
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
    
