from django.db import models
from django.core.urlresolvers import reverse
from gubbins.db.field import EnumField


class PageType(EnumField):
    RSS_FEED = 'rss_index'
    SITE_INDEX = 'site_index'
    PAGE = 'page'

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
    
    url = models.URLField(max_length=1000)
    scrape_every = models.IntegerField()
    enabled = models.BooleanField()
    page_source_type = PageType()

    def get_absolute_url(self):
        return reverse('scraper_page_detail', args=[self.id])
    
    def __unicode__(self):
        return self.name



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
    
