# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ScrapeAttempt.attempted_on'
        db.delete_column('scraping_scrapeattempt', 'attempted_on')


    def backwards(self, orm):
        # Adding field 'ScrapeAttempt.attempted_on'
        db.add_column('scraping_scrapeattempt', 'attempted_on',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 7, 10, 0, 0), blank=True),
                      keep_default=False)


    models = {
        'scraping.periodicscrape': {
            'Meta': {'object_name': 'PeriodicScrape', '_ormbases': ['scraping.ScraperPageBase']},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scrape_every': ('django.db.models.fields.IntegerField', [], {}),
            'scraperpagebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['scraping.ScraperPageBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'scraping.scrapeattempt': {
            'Meta': {'object_name': 'ScrapeAttempt'},
            'completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'error_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scraping.ScraperPageBase']"}),
            'started': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'state': ('scraping.models.ScrapeStatus', [], {})
        },
        'scraping.scraperpage': {
            'Meta': {'object_name': 'ScraperPage', '_ormbases': ['scraping.ScraperPageBase']},
            'scraperpagebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['scraping.ScraperPageBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'scraping.scraperpagebase': {
            'Meta': {'object_name': 'ScraperPageBase'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_type': ('scraping.models.PageType', [], {}),
            'scraper': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['scraping']