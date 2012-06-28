
from django.contrib import admin
from scraping.models import ScraperPage, ScrapeAttempt, PeriodicScrape


class ScraperPageAdmin(admin.ModelAdmin):
    search_fields = ('url',)


admin.site.register(ScraperPage, ScraperPageAdmin)
admin.site.register(PeriodicScrape, ScraperPageAdmin)

admin.site.register(ScrapeAttempt)
#class ParseFailureAdmin(admin.ModelAdmin):
#    readonly_fields = ('scraper_page',)
#    search_fields = ('scraper_page__url',)
#admin.site.register(ParseFailure, ParseFailureAdmin)

