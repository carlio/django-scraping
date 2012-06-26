from django.db import models
from django.core.urlresolvers import reverse
from gubbins.db.fields import EnumField


class PageSourceType(EnumField):
    FISH = 'fish'
    pass



class ScraperPageSource(models.Model):
    """
    This model represents the initial source of scraper pages.
    
    One example use case is an RSS feed, which simply lists new pages
    to be scraped. Another is the index page of a news site, which would
    be periodically checked and new links to news articles or other index
    pages would be started.
    """
    
    url = models.URLField(max_length=1000)
    scrape_every = models.IntegerField()

    page_source_type = PageSourceType()


class ScraperPage(models.Model):
    
    url = models.URLField(max_length=1000)
    last_scrape = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField()
    
    def get_absolute_url(self):
        return reverse('scraper_page_detail', args=[self.id])
    
    def __unicode__(self):
        return self.name

    

class ParseFailure(models.Model):
    
    scraper_page = models.ForeignKey(ScraperPage)
    parse_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    
    def __init__(self, *args, **kwargs):
        super(ParseFailure, self).__init__(*args, **kwargs)
        
    def get_summary(self):
        lines = self.message.split('\n')
        lines = filter(lambda x:x.strip()!='', lines)
        
        if len(lines) <= 1:
            return self.message
        
        return '\n'.join( lines[-3:] )
    
    def __unicode__(self):
        return u'failure parsing %s' % self.scraper_page
    
