# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ContentNode.dateCreated'
        db.add_column(u'base_contentnode', 'dateCreated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=None, blank=True),
                      keep_default=False)

        # Adding field 'ContentNode.dateModified'
        db.add_column(u'base_contentnode', 'dateModified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=None, blank=True),
                      keep_default=False)

        # Adding field 'Link.dateCreated'
        db.add_column(u'base_link', 'dateCreated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=None, blank=True),
                      keep_default=False)

        # Adding field 'Link.dateModified'
        db.add_column(u'base_link', 'dateModified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=None, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ContentNode.dateCreated'
        db.delete_column(u'base_contentnode', 'dateCreated')

        # Deleting field 'ContentNode.dateModified'
        db.delete_column(u'base_contentnode', 'dateModified')

        # Deleting field 'Link.dateCreated'
        db.delete_column(u'base_link', 'dateCreated')

        # Deleting field 'Link.dateModified'
        db.delete_column(u'base_link', 'dateModified')


    models = {
        u'base.contentnode': {
            'Meta': {'object_name': 'ContentNode'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'dateCreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dateModified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'dateCreated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dateModified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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