from annoying.decorators import render_to
from collections import defaultdict
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from celery.task import control
import urllib
from scraping.models import ScraperPage


class RescrapeForm(forms.Form):
    start_idx = forms.IntegerField(initial=0)
    count = forms.IntegerField(required=False, help_text='Leave blank to parse all')
    use_cache = forms.BooleanField(initial=True, required=False)
    fetch_if_missing = forms.BooleanField(initial=True, required=False)
    failed_only = forms.BooleanField(initial=True, required=False)
    

@login_required
@render_to('scraper/parse_controls.html')
def parse_controls(request):
    
    rescrape_form = RescrapeForm()
    
    if request.method == 'POST':
        if request.POST['type'] == 'rescrape':
            rescrape_form = RescrapeForm(request.POST)
            if rescrape_form.is_valid():
                qs = ScraperPage.objects.filter(page_type__in=rescrape_form.cleaned_data['page_types'])
                if rescrape_form.cleaned_data['failed_only']:
                    qs = qs.filter(success=False)
                
                start_idx = rescrape_form.cleaned_data['start_idx']
                count = rescrape_form.cleaned_data['count']
                if count is None:
                    qs = qs[start_idx:]
                else:
                    qs = qs[start_idx:start_idx+count]
                
                for page in qs:
                    parse_page(page, rescrape_form.cleaned_data['use_cache'], rescrape_form.cleaned_data['fetch_if_missing'])
                    
                messages.info(request, 'Rescraping %s pages' % qs.count() )
                return redirect(reverse('parse_controls'))
            
        if request.POST['type'] == 'general':
            if 'boobpedia-index' in request.POST:
                boobpedia.parse_index_page.delay()
                messages.info(request, 'Scraping Boobpedia')
            if 'chickipedia-index' in request.POST:
                chickipedia.parse_index.delay()
                messages.info(request, 'Scraping Chickipedia')
            if 'aliases' in request.POST:
                deal_with_aliases.delay()
                messages.info(request, 'Dealing with aliases')
            if 'baberank' in request.POST:
                scrape_baberank.delay()
                messages.info(request, 'Scraping freeones baberank')
            if 'report' in request.POST:
                report.delay()
                messages.info(request, 'Generating report')
            if 'discover-freeones' in request.POST:
                discover_all_freeones.delay()
                messages.info(request, 'Finding all Freeones galleries')
    
    return {'rescrape_form': rescrape_form}
    
    
class CacheForm(forms.Form):
    url = forms.CharField()


@login_required
@render_to('scraper/cache_controls.html')
def cache_controls(request):
    ctx = {}
    
    cache_form = CacheForm()
    if request.method == 'POST':
        if request.POST['type'] == 'view':
            cache_form = CacheForm(request.POST)
            if cache_form.is_valid():
                url = cache_form.cleaned_data['url']
                ctx['html'], ctx['real_url'] = cache.get_html(url)
    
    else:
        cache_form = CacheForm(request.GET)
        if cache_form.is_valid():
            url = cache_form.cleaned_data['url']
            ctx['html'] = cache.get_html(url)
    
    ctx['cache_form'] = cache_form
    
    request_count, hit_count = cache.get_stats()
    if request_count == 0:
        hit_pc = 0
    else:
        hit_pc = 100 * hit_count / request_count
    ctx.update( {'cache_size': cache.get_size(), 'hit_pc': hit_pc, 
            'request_count': request_count, 'hit_count': hit_count } )
    
    return ctx
    


@login_required
@render_to('scraper/index.html')
def scraper_index(request):
    return {}


@login_required
@render_to('scraper/parse_failure_list.html')
def parse_failure_list(request):
    
    if request.method == 'POST' and request.user.is_superuser:
        failure_ids = request.POST['failure_ids'].split(',')
        for fid in failure_ids:
            failure = ParseFailure.objects.get(id=fid)
            parse_page(failure.scraper_page)
            failure.delete()
        messages.info(request, 'Rescraping %s pages' % len(failure_ids) )
    
    failures = ParseFailure.objects.all()
    
    groups = defaultdict(list)
    for failure in failures:
        groups[failure.get_summary()].append(failure.id)
    
    groups_sorted = sorted(groups.iteritems(), key=lambda x:-len(x[1]))
    
    return {'groups': groups_sorted}


@login_required
@render_to('scraper/parse_failure_detail.html')
def parse_failure_detail(request, failure_id):
    failure = get_object_or_404(ParseFailure, pk=failure_id)
    failures = ParseFailure.objects.filter(message=failure.message)
    
    if request.method == 'POST' and request.user.is_superuser:
        failure = ParseFailure.objects.get(pk=request.POST['failure_id'])
        parse_page(failure.scraper_page)
        messages.info(request, 'Rescraping page for %s' % failure.scraper_page.name )
        failure.delete()
    
    return {'failures': failures, 'canonical_tb': failure.message}


@login_required
@render_to('scraper/page_detail.html')
def page_detail(request, page_id):
    page = get_object_or_404(ScraperPage, pk=page_id)
    
    if request.method == 'POST' and request.user.is_superuser and 'scrape' in request.POST:
        parse_page(page)
        messages.info(request, 'Parse job added')
    
    params = {'url': page.get_scrape_url() }
    params = urllib.urlencode(params)
    cache_url = '%s?%s' % (reverse('cache_controls'), params)
    
    return {'page': page, 'cache_url': cache_url}



@login_required
@render_to('scraper/worker.html')
def worker_controls(request):
    i = control.inspect()
    return { 'active': i.active() }



@login_required
@render_to('scraper/stats.html')
def stats(request):
    total = Girl.objects.all().count()
    girl_stats = [ ('Total', total) ]
    
    for field in Girl._meta.fields:
        count = Girl.objects.exclude(**{field.name: None}).count()
        if total != 0:
            pc = 100*count / total
        else:
            pc = 0
        girl_stats.append( (field.name, '%d (%d%%)' % (count, pc)) )
        
    pic_stats = [ ('Total', Picture.objects.all().count() ),
                  ('Original', Picture.objects.filter(image_type=ImageType.ORIGINAL).count() ),
                  ('Thumbnail', Picture.objects.filter(image_type=ImageType.THUMB).count() ),
                  ('Advert', Picture.objects.filter(image_type=ImageType.ADVERT).count() ),
                  ('Large', Picture.objects.filter(image_type=ImageType.LARGE).count() ),
                  ('Average height', Picture.objects.all().aggregate(Avg('height'))['height__avg'] ),
                  ('Average width', Picture.objects.all().aggregate(Avg('width'))['width__avg'] )
                ]
    
    return {'girl_stats': girl_stats, 'pic_stats': pic_stats }