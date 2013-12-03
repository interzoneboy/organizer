# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NodeType'
        db.create_table(u'base_nodetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'base', ['NodeType'])

        # Adding model 'ContentNode'
        db.create_table(u'base_contentnode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('nodeType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.NodeType'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'base', ['ContentNode'])

        # Adding model 'LinkType'
        db.create_table(u'base_linktype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'base', ['LinkType'])

        # Adding model 'Link'
        db.create_table(u'base_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('linkType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.LinkType'])),
            ('pointA', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='aLinks', null=True, to=orm['base.ContentNode'])),
            ('pointB', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='bLinks', null=True, to=orm['base.ContentNode'])),
            ('direct', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('aPosX', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('aPosY', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('bPosX', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('bPosY', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['Link'])


    def backwards(self, orm):
        # Deleting model 'NodeType'
        db.delete_table(u'base_nodetype')

        # Deleting model 'ContentNode'
        db.delete_table(u'base_contentnode')

        # Deleting model 'LinkType'
        db.delete_table(u'base_linktype')

        # Deleting model 'Link'
        db.delete_table(u'base_link')


    models = {
        u'base.contentnode': {
            'Meta': {'object_name': 'ContentNode'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'nodeType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.NodeType']"})
        },
        u'base.link': {
            'Meta': {'object_name': 'Link'},
            'aPosX': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'aPosY': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bPosX': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bPosY': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'direct': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.LinkType']"}),
            'pointA': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'aLinks'", 'null': 'True', 'to': u"orm['base.ContentNode']"}),
            'pointB': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bLinks'", 'null': 'True', 'to': u"orm['base.ContentNode']"})
        },
        u'base.linktype': {
            'Meta': {'object_name': 'LinkType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'base.nodetype': {
            'Meta': {'object_name': 'NodeType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['base']