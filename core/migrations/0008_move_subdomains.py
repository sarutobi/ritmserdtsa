# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models, connection

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        cursor = connection.cursor()
        cursor.execute('insert into core_subdomain select * from subdomain')
        cursor.execute('''select setval('core_subdomain_id_seq', (select max(id) from core_subdomain))''')

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'core.category': {
            'Meta': {'ordering': "['order']", 'object_name': 'Category'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'#000000'", 'max_length': '7', 'db_column': "'color'"}),
            'description': ('django.db.models.fields.TextField', [], {'db_column': "'description'", 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.CategoryGroup']", 'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'icon'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_column': "'name'"}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'db_column': "'order'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_column': "'slug'", 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Subdomain']", 'null': 'True', 'db_column': "'subdomain_id'", 'blank': 'True'})
        },
        u'core.categorygroup': {
            'Meta': {'ordering': "['order']", 'object_name': 'CategoryGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.infopage': {
            'Meta': {'object_name': 'Infopage'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'db_column': "'text'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'title'"})
        },
        u'core.subdomain': {
            'Meta': {'ordering': "['order']", 'object_name': 'Subdomain'},
            'disclaimer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isCurrent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_current'"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']
    symmetrical = True
