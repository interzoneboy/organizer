# Models that are going to be used to store nodes and links in
# our information graph. We start with a structure that's as generic as possible save for
# the separation for the type-level classes like likeType and nodeType. These could also be implemented
# as normal links to normal nodes, but since there's going to be a LOT of filtering done on type, depending
# on what we want to do (look at graph, hierarch list gtd tasks, aggregate todos and notes, store and serve
# documentation, read, parse, and store files  and filecontents, be a good heads-up-display for
# analysis and for running servers, ...

import json
from django.db import models
from django.template import Template
from django.template import Context

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

    def getDiv(self):
        ret = self.nodeType.name
        if len(self.content) > 45:
            ret += (": " + self.name + ": " + self.content[0:45] + " ...")
        else:
            ret += (": " + self.name + ": " + self.content[0:45])
        return(ret)

    def __unicode__(self):
        return u'%s: %s' % (self.name, str(self.nodeType))


def render(node, templateContent):
    t = Template(template.content)
    contextObj = json.loads(node.content)
    contextObj.update({'node':node})
    c = Context(contextObj)
    return(t.render(c))

def renderEdit(node_id):
    theNode = ContentNode.objects.get(id=node_id)
    extraStuff = ContentNode.objects.raw("""SELECT cn.id,
                                             cn.nodetype_id,
                                             cn.content,
                                             cnn.id,
                                             cnn.content AS templateContent
                                             FROM base_contentnode cn
                                             LEFT JOIN base_link ll ON cn.id=ll.pointA_id
                                                   AND ll.linktype_id IN (SELECT id from base_linktype WHERE name="gtd_edit_template")
                                             LEFT JOIN base_contentnode cnn ON ll.pointB_id=ccn.id
                                             WHERE cn.id = %s
                                   ;""", [node_id])
    return(render(theNode, extraStuff.templateContent))



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
    
    def getDiv(self):
        ret = self.linkType.name +": "+self.pointA.name + " -> " + self.pointB.name
        return(ret)

    def __unicode__(self):
        return u'%s: %s -- %s, %s' % (str(self.linkType),
                                      str(self.pointA),
                                      str(self.pointB),
                                      str(self.direct))
    
        
