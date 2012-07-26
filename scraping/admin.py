
from django.contrib import admin
from scraping.models import ScraperPage, ScrapeAttempt, PeriodicScrape
from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.forms.util import flatatt


def schedule_scrape(modeladmin, request, queryset):
    for page in queryset:
        page.schedule_scrape()
schedule_scrape.short_description = 'Schedule scrape'


class ScraperPageAdmin(admin.ModelAdmin):
    search_fields = ('url',)
    actions = [schedule_scrape]


admin.site.register(ScraperPage, ScraperPageAdmin)
admin.site.register(PeriodicScrape, ScraperPageAdmin)


def reschedule_scrape_attempt(modeladmin, request, queryset):
    for attempt in queryset:
        attempt.reschedule()
reschedule_scrape_attempt.short_description = 'Reschedule selected pages'




class CodeWidget(forms.Textarea):
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        print 'alalala'
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<br/><pre%s>%s</pre>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))))

class ScrapeAttemptForm(forms.ModelForm):
    class Meta:
        model = ScrapeAttempt
        widgets = {
            'error_message': CodeWidget()       
        }

class ScrapeAttemptAdmin(admin.ModelAdmin):
    search_fields = ('page__url',)
    list_filter = ('started', 'completed', 'state')
    list_display = ('get_page_url', 'started', 'completed', 'state', 'time_taken')
    readonly_fields = ('page', 'state', 'completed')
    fields = ('page', 'state', 'completed', 'error_message')
    actions = [reschedule_scrape_attempt]
    form = ScrapeAttemptForm


admin.site.register(ScrapeAttempt, ScrapeAttemptAdmin)

