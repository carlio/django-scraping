from django.conf import settings
import requests


def fetch_url(url):
    user_agent = getattr(settings, 'SCRAPER_USER_AGENT', 'django-scraping v0.1')
    headers = { 'User-Agent': user_agent }
    
    resp = requests.get(url, headers=headers, timeout=30)
    return resp.text, resp.url
