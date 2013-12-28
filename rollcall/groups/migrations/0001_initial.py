# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table(u'groups_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=50, populate_from='name', unique_with=())),
        ))
        db.send_create_signal(u'groups', ['Group'])

        # Adding M2M table for field sublists on 'Group'
        m2m_table_name = db.shorten_name(u'groups_group_sublists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_group', models.ForeignKey(orm[u'groups.group'], null=False)),
            ('to_group', models.ForeignKey(orm[u'groups.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_group_id', 'to_group_id'])

        # Adding model 'Membership'
        db.create_table(u'groups_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groups.Group'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'groups', ['Membership'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table(u'groups_group')

        # Removing M2M table for field sublists on 'Group'
        db.delete_table(db.shorten_name(u'groups_group_sublists'))

        # Deleting model 'Membership'
        db.delete_table(u'groups_membership')


    models = {
        u'groups.group': {
            'Meta': {'object_name': 'Group'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['people.Person']", 'through': u"orm['groups.Membership']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
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