# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ScraperPageBase.scraper'
        db.add_column('scraping_scraperpagebase', 'scraper',
                      self.gf('django.db.models.fields.CharField')(default='default', max_length=100),
                      keep_default=False)


        # Changing field 'ScraperPageBase.page_type'
        db.alter_column('scraping_scraperpagebase', 'page_type', self.gf('scraping.models.PageType')())

    def backwards(self, orm):
        # Deleting field 'ScraperPageBase.scraper'
        db.delete_column('scraping_scraperpagebase', 'scraper')


        # Changing field 'ScraperPageBase.page_type'
        db.alter_column('scraping_scraperpagebase', 'page_type', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        'scraping.periodicscrape': {
            'Meta': {'object_name': 'PeriodicScrape', '_ormbases': ['scraping.ScraperPageBase']},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scrape_every': ('django.db.models.fields.IntegerField', [], {}),
            'scraperpagebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['scraping.ScraperPageBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'scraping.scrapeattempt': {
            'Meta': {'object_name': 'ScrapeAttempt'},
            'attempted_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scraping.ScraperPageBase']"}),
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