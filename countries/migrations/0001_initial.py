# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('countries_country', (
            ('iso', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name_es', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('printable_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('printable_name_es', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('printable_name_en', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('iso3', self.gf('django.db.models.fields.CharField')(max_length=3, null=True)),
            ('numcode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
        ))
        db.send_create_signal('countries', ['Country'])

        # Adding model 'UsState'
        db.create_table('countries_usstate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('abbrev', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('countries', ['UsState'])

        # Adding model 'Province'
        db.create_table('countries_province', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='provinces', to=orm['countries.Country'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('countries', ['Province'])


    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table('countries_country')

        # Deleting model 'UsState'
        db.delete_table('countries_usstate')

        # Deleting model 'Province'
        db.delete_table('countries_province')


    models = {
        'countries.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country'},
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'numcode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'printable_name_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'printable_name_es': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'countries.province': {
            'Meta': {'ordering': "['country', 'name']", 'object_name': 'Province'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'provinces'", 'to': "orm['countries.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'countries.usstate': {
            'Meta': {'ordering': "('name',)", 'object_name': 'UsState'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['countries']
