from django.core.urlresolvers import reverse
from django.db import models
from gubbins.db.field import EnumField
from gubbins.db.manager import InheritanceManager


class ScrapeStatus(EnumField):
    IN_PROGRESS = 'in_progress'
    SUCCESS = 'success'
    FAILURE = 'failure'



class ScraperPage(models.Model):
    """
    This model represents the initial source of scraper pages.
    
    One example use case is an RSS feed, which simply lists new pages
    to be scraped. Another is the index page of a news site, which would
    be periodically checked and new links to news articles or other index
    pages would be started.
    """
    objects = InheritanceManager()
    
    url = models.URLField(max_length=1000)

    def get_absolute_url(self):
        return reverse('scraper_page_detail', args=[self.id])
    
    def get_last_scrape(self):
        attempts = self.scrapeattempt_set.order_by('-attempted_on')
        if attempts.count() == 0:
            return None
        return attempts[0]
    
    def __unicode__(self):
        return self.url


class PeriodicScrape(ScraperPage):

    scrape_every = models.IntegerField()
    enabled = models.BooleanField()



class ScrapeAttempt(models.Model):
    attempted_on = models.DateTimeField(auto_now_add=True)
    state = ScrapeStatus(default=ScrapeStatus.IN_PROGRESS)
    page = models.ForeignKey(ScraperPage)
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
    
