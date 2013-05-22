# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models, connection

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        move_locations = '''
        insert into geozones_location(id, latitude, longitude, region_id, description)
        select id, latitude, longtitude, region_id, name from "Location"
        '''
        fix_location_id = '''
        select setval('geozones_location_id_seq', (select max(id) from geozones_location))
        '''
        cursor = connection.cursor()
        cursor.execute(move_locations)
        cursor.execute(fix_location_id)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'geozones.location': {
            'Meta': {'object_name': 'Location'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {'db_column': "'longitude'"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geozones.Region']", 'null': 'True', 'blank': 'True'})
        },
        u'geozones.region': {
            'Meta': {'ordering': "['order']", 'object_name': 'Region'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'zoom': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['geozones']
    symmetrical = True
