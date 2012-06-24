
from django.contrib import admin
from scraping.models import ScraperPage, ParseFailure

class ScraperPageAdmin(admin.ModelAdmin):
    search_fields = ('url',)
    list_filter = ('success', 'last_scrape')

admin.site.register(ScraperPage, ScraperPageAdmin)

class ParseFailureAdmin(admin.ModelAdmin):
    readonly_fields = ('scraper_page',)
    search_fields = ('scraper_page__url',)
admin.site.register(ParseFailure, ParseFailureAdmin)

