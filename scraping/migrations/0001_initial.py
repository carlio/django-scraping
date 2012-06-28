# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ScraperPageBase'
        db.create_table('scraping_scraperpagebase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=1000)),
        ))
        db.send_create_signal('scraping', ['ScraperPageBase'])

        # Adding model 'ScraperPage'
        db.create_table('scraping_scraperpage', (
            ('scraperpagebase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['scraping.ScraperPageBase'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('scraping', ['ScraperPage'])

        # Adding model 'PeriodicScrape'
        db.create_table('scraping_periodicscrape', (
            ('scraperpagebase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['scraping.ScraperPageBase'], unique=True, primary_key=True)),
            ('scrape_every', self.gf('django.db.models.fields.IntegerField')()),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('scraping', ['PeriodicScrape'])

        # Adding model 'ScrapeAttempt'
        db.create_table('scraping_scrapeattempt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attempted_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('state', self.gf('scraping.models.ScrapeStatus')()),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scraping.ScraperPageBase'])),
            ('error_message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('scraping', ['ScrapeAttempt'])


    def backwards(self, orm):
        # Deleting model 'ScraperPageBase'
        db.delete_table('scraping_scraperpagebase')

        # Deleting model 'ScraperPage'
        db.delete_table('scraping_scraperpage')

        # Deleting model 'PeriodicScrape'
        db.delete_table('scraping_periodicscrape')

        # Deleting model 'ScrapeAttempt'
        db.delete_table('scraping_scrapeattempt')


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
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['scraping']