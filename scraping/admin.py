
from django.contrib import admin
from scraping.models import ScraperPage, ScrapeAttempt, PeriodicScrape


class ScraperPageAdmin(admin.ModelAdmin):
    search_fields = ('url',)


admin.site.register(ScraperPage, ScraperPageAdmin)
admin.site.register(PeriodicScrape, ScraperPageAdmin)


class ScrapeAttemptAdmin(admin.ModelAdmin):
    search_fields = ('page__url',)
    list_filter = ('started', 'completed', 'state')
    list_display = ('get_page_url', 'started', 'completed', 'state', 'time_taken')
    
admin.site.register(ScrapeAttempt, ScrapeAttemptAdmin)

