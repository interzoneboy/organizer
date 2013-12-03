# Models that are going to be used to store nodes and links in
# our information graph. We start with a structure that's as generic as possible save for
# the separation for the type-level classes like likeType and nodeType. These could also be implemented
# as normal links to normal nodes, but since there's going to be a LOT of filtering done on type, depending
# on what we want to do (look at graph, hierarch list gtd tasks, aggregate todos and notes, store and serve
# documentation, read, parse, and store files  and filecontents, be a good heads-up-display for
# analysis and for running servers, ...

import json
from django.db import models

# Create your models here.

class NodeType(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def getDict(self):
        d = {'name':self.name}
        return(d)

    def getJson(self):
        dStr = json.dumps(self.getDict())
        return(dStr)
        
    def __unicode__(self):
        return u'%s' % (self.name,)


class ContentNode(models.Model):

    name = models.CharField(max_length=200, unique=True)
    nodeType = models.ForeignKey('NodeType')
    content = models.TextField()
    
    def getDict(self):
        d = {'name':self.name, 'nodeType':self.nodeType.getDict(), 'content':self.content}
        return(d)
    def getJson(self):
        dStr = json.dumps(self.getDict())
        return(dStr)

    def __unicode__(self):
        return u'%s: %s' % (self.name, str(self.nodeType))



class LinkType(models.Model):

    name = models.CharField(max_length=100, unique=True)
    def getDict(self):
        d = {'name':self.name}
        return(d)

    def getJson(self):
        dStr = json.dumps(self.getDict())
        return(dStr)

    def __unicode__(self):
        return u'%s' % (self.name,)
        
class Link(models.Model):
    linkType = models.ForeignKey('LinkType')
    pointA = models.ForeignKey('ContentNode', blank=True, null=True, related_name="aLinks")
    pointB = models.ForeignKey('ContentNode', blank=True, null=True, related_name="bLinks")
    direct = models.CharField(max_length=2, choices=(("n","n"),("a","a"),("b","b")))
    aPosX = models.IntegerField(blank=True, null=True)
    aPosY = models.IntegerField(blank=True, null=True)
    bPosX = models.IntegerField(blank=True, null=True)
    bPosY = models.IntegerField(blank=True, null=True)
    
    def getDict(self):
        d = {'a':self.pointA.getDict(), 'b':self.pointB.getDict(), 'direct':self.direct,
             'aPosX':self.aPosX, 'aPosY':self.aPosY, 'bPosX':self.bPosX, 'bPosY':self.bPosY, 
             'linkType':self.linkType.getDict()}
        return(d)

    def getJson(self):
        dStr = json.dumps(self.getDict())
        return(dStr)

    def __unicode__(self):
        return u'%s: %s -- %s, %s' % (str(self.linkType),
                                      str(self.pointA),
                                      str(self.pointB),
                                      str(self.direct))
    
        
