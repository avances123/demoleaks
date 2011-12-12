# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Comicio'
        db.create_table('electoral_comicio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nombre_es', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('nombre_en', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, db_index=True)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comicios', to=orm['countries.Country'])),
            ('fecha', self.gf('django.db.models.fields.DateField')(null=True)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('sitio', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comicios', null=True, to=orm['electoral.Sitio'])),
        ))
        db.send_create_signal('electoral', ['Comicio'])

        # Adding model 'Sitio'
        db.create_table('electoral_sitio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codigo_ISO_3166', self.gf('django.db.models.fields.CharField')(max_length=8, null=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nombre_es', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('nombre_en', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, db_index=True)),
            ('num_a_elegir', self.gf('django.db.models.fields.IntegerField')()),
            ('tipo', self.gf('django.db.models.fields.IntegerField')()),
            ('votos_contabilizados', self.gf('django.db.models.fields.IntegerField')()),
            ('votos_abstenciones', self.gf('django.db.models.fields.IntegerField')()),
            ('votos_nulos', self.gf('django.db.models.fields.IntegerField')()),
            ('votos_blancos', self.gf('django.db.models.fields.IntegerField')()),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='sitios', null=True, to=orm['electoral.Sitio'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('electoral', ['Sitio'])

        # Adding model 'Partido'
        db.create_table('electoral_partido', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sitio', self.gf('django.db.models.fields.related.ForeignKey')(related_name='partidos', to=orm['electoral.Sitio'])),
            ('id_partido', self.gf('django.db.models.fields.IntegerField')()),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nombre_es', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('nombre_en', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, db_index=True)),
            ('electos', self.gf('django.db.models.fields.IntegerField')()),
            ('votos_numero', self.gf('django.db.models.fields.IntegerField')()),
            ('votos_porciento', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('electoral', ['Partido'])


    def backwards(self, orm):
        
        # Deleting model 'Comicio'
        db.delete_table('electoral_comicio')

        # Deleting model 'Sitio'
        db.delete_table('electoral_sitio')

        # Deleting model 'Partido'
        db.delete_table('electoral_partido')


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
        'electoral.comicio': {
            'Meta': {'ordering': "['pais', 'nombre']", 'object_name': 'Comicio'},
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nombre_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nombre_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comicios'", 'to': "orm['countries.Country']"}),
            'sitio': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comicios'", 'null': 'True', 'to': "orm['electoral.Sitio']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'electoral.partido': {
            'Meta': {'ordering': "['nombre', 'sitio']", 'object_name': 'Partido'},
            'electos': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_partido': ('django.db.models.fields.IntegerField', [], {}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nombre_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nombre_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'sitio': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'partidos'", 'to': "orm['electoral.Sitio']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'}),
            'votos_numero': ('django.db.models.fields.IntegerField', [], {}),
            'votos_porciento': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        'electoral.sitio': {
            'Meta': {'ordering': "['nombre']", 'object_name': 'Sitio'},
            'codigo_ISO_3166': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nombre_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nombre_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_a_elegir': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'sitios'", 'null': 'True', 'to': "orm['electoral.Sitio']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'votos_abstenciones': ('django.db.models.fields.IntegerField', [], {}),
            'votos_blancos': ('django.db.models.fields.IntegerField', [], {}),
            'votos_contabilizados': ('django.db.models.fields.IntegerField', [], {}),
            'votos_nulos': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['electoral']