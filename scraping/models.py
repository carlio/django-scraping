from django.db import models
from django.core.urlresolvers import reverse


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
    
