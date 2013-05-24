# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models, connection

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        move_messages = '''
        insert into message_message(
        id, title, message,
        contact_first_name, contact_last_name, contact_mail, contact_phone,
        message_type, status, date_add, date_modify, user_id, subdomain_id,
        linked_location_id, location, georegion_id, address,
        is_active, is_important, is_anonymous, is_removed, allow_feedback
        )
        SELECT m.id, m.title, m.message,
        (xpath('/sender/firstname/text()[1]'::text, m.sender))[1]::character varying(100),
        case 
        when (xpath('/sender/lastname/text()[1]'::text, m.sender))[1]::character varying(100) is null then ''
        else (xpath('/sender/lastname/text()[1]'::text, m.sender))[1]::character varying(100) end,
        case
        when (xpath('/sender/email/text()[1]'::text, m.sender))[1]::character varying(100) is null then ''
        else (xpath('/sender/email/text()[1]'::text, m.sender))[1]::character varying(100)
        end,
        xpath('/sender/phone/text()'::text, m.sender)::character varying(12)[],
        m.message_type, m.status, m.date_add, m.date_modify, m.user_id, m.subdomain_id,
        l.id, geomfromtext('POINT(' || l.longtitude || ' ' || l.latitude || ')', 4326), l.region_id, l.name,
        m.flags & 1::bigint = 1,
        (m.flags & 2::bigint) >> 1 = 1,
        (m.flags & 4::bigint) >> 2 != 1,
        (m.flags & 16::bigint) >> 4 = 1,
        (m.flags & 8::bigint) >> 3 = 1
        FROM "Message" m
        JOIN "Location" l ON m.location_id = l.id
        LEFT JOIN "Region" r ON l.region_id = r.id
        LEFT JOIN subdomain s ON m.subdomain_id = s.id
        '''
        fix_message_id = '''
        select setval('message_message_id_seq', (select max(id) from message_message))
        '''
        cursor = connection.cursor()
        cursor.execute(move_messages)
        cursor.execute(fix_message_id)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        u'core.subdomain': {
            'Meta': {'ordering': "['order']", 'object_name': 'Subdomain'},
            'disclaimer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isCurrent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_current'"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
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
        },
        u'message.message': {
            'Meta': {'ordering': "['-date_add']", 'object_name': 'Message'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'allow_feedback': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Category']", 'null': 'True', 'db_table': "'messagecategories'", 'blank': 'True'}),
            'contact_first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'contact_last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'contact_mail': ('django.db.models.fields.EmailField', [], {'max_length': '200', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_column': "'date_add'", 'blank': 'True'}),
            'edit_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'expired_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'georegion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geozones.Region']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_important': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_edit': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_column': "'date_modify'", 'blank': 'True'}),
            'linked_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geozones.Location']", 'null': 'True', 'blank': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'messageType': ('django.db.models.fields.IntegerField', [], {'db_column': "'message_type'"}),
            'sender_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Subdomain']", 'null': 'True', 'db_column': "'subdomain_id'", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'db_column': "'user_id'", 'blank': 'True'})
        },
        u'message.messagenotes': {
            'Meta': {'object_name': 'MessageNotes'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edit': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['message.Message']"}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['message']
    symmetrical = True
