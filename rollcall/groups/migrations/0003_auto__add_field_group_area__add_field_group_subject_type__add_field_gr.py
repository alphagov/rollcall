# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Group.area'
        db.add_column(u'groups_group', 'area',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Group.subject_type'
        db.add_column(u'groups_group', 'subject_type',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Group.subject'
        db.add_column(u'groups_group', 'subject',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Group.list_type'
        db.add_column(u'groups_group', 'list_type',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Group.area'
        db.delete_column(u'groups_group', 'area')

        # Deleting field 'Group.subject_type'
        db.delete_column(u'groups_group', 'subject_type')

        # Deleting field 'Group.subject'
        db.delete_column(u'groups_group', 'subject')

        # Deleting field 'Group.list_type'
        db.delete_column(u'groups_group', 'list_type')


    models = {
        u'groups.group': {
            'Meta': {'object_name': 'Group'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['people.Person']", 'through': u"orm['groups.Membership']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'state': (u'dj.choices.fields.ChoiceField', [], {'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'blank': 'False', u'default': '1', 'null': 'False', '_in_south': 'True', 'db_index': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'sublists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['groups.Group']", 'null': 'True', 'blank': 'True'})
        },
        u'groups.membership': {
            'Meta': {'object_name': 'Membership'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['groups.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Person']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'people.person': {
            'Meta': {'object_name': 'Person'},
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'google_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'})
        }
    }

    complete_apps = ['groups']