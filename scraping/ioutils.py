from django.conf import settings
import urllib2
import re


def fetch_url(url):
    user_agent = getattr(settings, 'SCRAPER_USER_AGENT', 'django-scraping v0.1')
    headers = { 'User-Agent': user_agent }
    
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