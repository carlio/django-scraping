from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('boobdb.scraper.views',
    url(r'^$', 'scraper_index', name='scraper_index'),
    url(r'^parse$', 'parse_controls', name='parse_controls'),
    url(r'^cache$', 'cache_controls', name='cache_controls'),
    url(r'^worker$', 'worker_controls', name='worker_controls'),
    url(r'^stats$', 'stats', name='stats'),
    
    url(r'^failures$', 'parse_failure_list', name='parse_failure_list'),
    url(r'^failures/(?P<failure_id>\d+)$', 'parse_failure_detail', name='parse_failure_detail'),
    url(r'^page/(?P<page_id>\d+)$', 'page_detail', name='scraper_page_detail'),
)
