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
from django.template.loader import render_to_string

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
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    
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


def renderHelper(node, templateContent):
    t = Template(templateContent)
    try:
        contextObj = json.loads(node.content)
    except ValueError,e:
        contextObj = {}
    contextObj.update({'node':node})
    nodeTypeNames = NodeType.objects.all().values_list('name',flat=True)
    contextObj.update({'nodeTypes':nodeTypeNames, 'selectedName':node.nodeType.name})
    c = Context(contextObj)
    return(t.render(c))

class NoTemplateException(Exception):
    pass

def render(node_name, followLink="gtd_type", templateLink="gtd_edit_template", defaultTemplateName="no_template.ttml"):
    theNode = ContentNode.objects.get(name=node_name)
    def findTemplate(theNode):
        origNodes = []
        stack = [theNode]
        while len(stack) > 0:
            item = stack[0]
            print(item)
            if (len(origNodes) > 0) and (item in origNodes): # We've come around in a circle.
                raise NoTemplateException()

            origNodes.append(item)

            if templateLink in item.aLinks.all().values_list('linkType__name',flat=True):
                # do something nice
                templateNode = item.aLinks.filter(linkType__name=templateLink)[0].pointB
                return templateNode
            else:
                # get my gtd_child parent nodes
                parentNodes = [a.pointA for a in item.bLinks.all() if a.linkType.name==followLink]
                stack = stack[1:] + parentNodes

        raise NoTemplateException()

    try:
        extraStuff = findTemplate(theNode)
        return(renderHelper(theNode, extraStuff.content))
    except NoTemplateException,e:
        #return("<div>NO TEMPLATE AVAILABLE</div>")
        nodeTypeNames = NodeType.objects.all().values_list('name',flat=True)
        return(render_to_string(defaultTemplateName, {'node':theNode, 'nodeTypes':nodeTypeNames, 'selectedName':theNode.nodeType.name}))

def renderEdit(node_name):
    return render(node_name, "gtd_child", "gtd_edit_template", "defaultEditTemplate.ttml")

def renderAdd(node_name):
    return render(node_name, "gtd_child", "gtd_add_template", "defaultAddTemplate.ttml")

def renderView(node_name):
    return render(node_name, "gtd_child", "gtd_view_template", "defaultViewTemplate.ttml")


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
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
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
    
        
