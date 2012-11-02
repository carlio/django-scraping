from datetime import timedelta, datetime
from django.core.urlresolvers import reverse
from django.db import models
from gubbins.db.field import EnumField
from gubbins.db.manager import InheritanceManager
from django.utils import timezone
import logging
from scraping.ioutils import get_ffk, fetch


class ScrapeStatus(EnumField):
    IN_PROGRESS = 'in_progress'
    SUCCESS = 'success'
    FAILURE = 'failure'
    
class PageType(EnumField):
    RSS = 'rss'
    HTML = 'html'
    XML = 'xml'


class ScraperPageBase(models.Model):
    
    objects = InheritanceManager()
    
    url = models.URLField(max_length=1000, db_index=True)
    page_type = PageType(default=PageType.HTML) 
    scraper = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True)
    
    def schedule_scrape(self, use_cache=True, fetch_if_missing=True):
        ffk = get_ffk(use_cache, fetch_if_missing)
        attempt = ScrapeAttempt.objects.create(page=self)
        # we have to use the task name here to avoid circular imports between models.py and tasks.py...
        fetch.delay(self.url, ffk, 'scraping.tasks.handle_page_scrape', callback_kwargs={'scraper_page': self, 'attempt': attempt})
  
    def scrape(self, url, scraper, page_type=None):
        page_type = page_type or self.page_type
        page, _ = ScraperPage.objects.get_or_create(url=url, scraper=scraper, 
                                                    page_type=page_type, parent=self)
        page.schedule_scrape()
        return page
  
    def get_absolute_url(self):
        return reverse('scraper_page_detail', args=[self.id])
    
    def get_last_scrape(self):
        attempts = self.scrapeattempt_set.order_by('-started')
        if attempts.count() == 0:
            return None
        return attempts[0]
    
    def __unicode__(self):
        return self.url


class ScraperPage(ScraperPageBase):
    """
    This model represents the initial source of scraper pages.
    
    One example use case is an RSS feed, which simply lists new pages
    to be scraped. Another is the index page of a news site, which would
    be periodically checked and new links to news articles or other index
    pages would be started.
    """
    pass
    


class PeriodicScrape(ScraperPageBase):

    scrape_every = models.IntegerField()
    enabled = models.BooleanField()
    
    def scrape_due(self):
        last_scrape = self.get_last_scrape()
        
        if last_scrape is None:
            logging.debug('Never scraped before, so a scrape is due')
            return True
        
        if last_scrape.started + timedelta(seconds=self.scrape_every) < datetime.now():
            logging.debug('Last scrape was more than %s seconds ago, so a scrape is due' % self.scrape_every)
            return True
        
        logging.debug('Scrape is not due')
        return False
            
    def __unicode__(self):
        return '%s (%s, every %s seconds)' % (self.url, self.page_type, self.scrape_every)



class ScrapeAttempt(models.Model):
    started = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True)
    state = ScrapeStatus(default=ScrapeStatus.IN_PROGRESS)
    page = models.ForeignKey(ScraperPageBase)
    error_message = models.TextField(null=True, blank=True)

    @property
    def success(self):
        return self.state == ScrapeStatus.SUCCESS
    
    def complete(self, state=ScrapeStatus.SUCCESS, error_message=None):
        self.completed = timezone.now()
        self.error_message = error_message
        self.state = state
        self.save()
        
    def reschedule(self, use_cache=True, fetch_if_missing=True):
        self.page.schedule_scrape(use_cache, fetch_if_missing)
        
    def get_page_url(self):
        # required for the admin list display, since it can't handle "page__url"
        return self.page.url
    
    def get_summary(self):
        lines = self.message.split('\n')
        lines = filter(lambda x:x.strip()!='', lines)
        
        if len(lines) <= 1:
            return self.message
        
        return '\n'.join( lines[-3:] )
    
    def time_taken(self):
        if self.state not in (ScrapeStatus.FAILURE, ScrapeStatus.SUCCESS):
            return '-'
        diff = (self.completed - self.started)
        seconds_taken = '%d.%3d' % (diff.seconds, diff.microseconds/1000)
        return '%s seconds' % (seconds_taken)
    
    def __unicode__(self):
        return u'%s scrape for %s started on %s' % (self.get_state_display(), self.page, self.started)
    
