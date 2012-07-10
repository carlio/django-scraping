from datetime import timedelta, datetime
from django.core.urlresolvers import reverse
from django.db import models
from gubbins.db.field import EnumField
from gubbins.db.manager import InheritanceManager


class ScrapeStatus(EnumField):
    IN_PROGRESS = 'in_progress'
    SUCCESS = 'success'
    FAILURE = 'failure'
    
class PageType(EnumField):
    RSS = 'rss'
    HTML = 'html'


class ScraperPageBase(models.Model):
    
    objects = InheritanceManager()
    
    url = models.URLField(max_length=1000)
    page_type = PageType(default=PageType.HTML) 
    scraper = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('scraper_page_detail', args=[self.id])
    
    def get_last_scrape(self):
        attempts = self.scrapeattempt_set.order_by('-attempted_on')
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
            return True
        if last_scrape + timedelta(seconds=self.scrape_every) < datetime.now():
            return True
        return False
            
    def __unicode__(self):
        return '%s (%s, every %s seconds)' % (self.url, self.page_type, self.scrape_every)



class ScrapeAttempt(models.Model):
    attempted_on = models.DateTimeField(auto_now_add=True)
    state = ScrapeStatus(default=ScrapeStatus.IN_PROGRESS)
    page = models.ForeignKey(ScraperPageBase)
    error_message = models.TextField(null=True, blank=True)

    @property
    def success(self):
        return self.state == ScrapeStatus.SUCCESS
    
    def get_summary(self):
        lines = self.message.split('\n')
        lines = filter(lambda x:x.strip()!='', lines)
        
        if len(lines) <= 1:
            return self.message
        
        return '\n'.join( lines[-3:] )
    
    def __unicode__(self):
        return u'failure parsing %s' % self.scraper_page
    
