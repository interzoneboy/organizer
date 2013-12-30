# The view functions described here are the "api" or more accurately the interface
# through which the database storage and data persistence will be done. The functions
# in this model will return Nodes, Links, and Graphs (as lists) for use in html templates,
# d3/other js, and anywhere else.
#
# [a for a in ...] comprehension structure is used so that actual lists of objects are returned
# from these functions, not unexecuted django querysets.
#
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
from base.models import ContentNode, NodeType
from base.models import Link, LinkType
from django.db.models import Q
import json


# Create your views here.

def getAllNodes_json():
    # ALL of them.
    allNodes = [a.getJson() for a in ContentNode.objects.all()]
    return(allNodes)

def getAllLinks_json():
    # ALL of these also.
    allLinks = [a.getJson() for a in Link.objects.all()]
    return(allLinks)


def getGraphFrom_json(nodeID, linkTypeID=None):
    # nodeID is a primary key from the node table, and indicates which node to use as the root
    # for this retrieval. This will put the "nodeID" root at the "root" position (whatever that means for the
    # visualization being used -- from our perspective it just means the node is the first in the list of nodes
    # returned by this function.
    pass

def getGraph(request):
    # Let's just get the graphs nodes, figure out what the indices in the list should be (?), then consult the links
    # and populate a link structure using the indices. The node array and link array must minimally conform to the
    # specifications for a d3 force directed layout.
    # ::TODO:: figure out how the position in the node list affects the layout. Is the first node always the root (eg?)
    allNodes = [a for a in ContentNode.objects.all()]
    allLinks = [a for a in Link.objects.all()]

    # We sort the list of nodes (for no real reason, now), and we use the calcLinkIndices helper function to compute
    # the indexes in the list of the nodes that are referred to in Links.
    allNodes_dicts = [{'index':a.id, 'name':a.name} for a in sorted(allNodes,key=lambda x: x.id)]
    def calcLinkIndices(ll):
        fromInd = [z['index'] for z in allNodes_dicts].index(ll.pointA_id)
        toInd = [z['index'] for z in allNodes_dicts].index(ll.pointB_id)
        return {'source':fromInd, 'target':toInd}
    
    allLinks_dicts = [calcLinkIndices(a) for a in allLinks]
    retDict = {'nodes':allNodes_dicts, 'links':allLinks_dicts}
    return HttpResponse(json.dumps(retDict), mimetype='application/json')

def addLink(request):
    """

    """
    response = {}
    if request.method=="POST":
        try:
            l_from = request.POST['from']
            l_to = request.POST['to']
            l_type = request.POST['type']
            linkType = LinkType.objects.get(name=l_type)
            fromNode = ContentNode.objects.get(name=l_from)
            toNode = ContentNode.objects.get(name=l_to)
            linky = Link(linkType=linkType,
                         pointA=fromNode,
                         pointB=toNode,
                         direct="b")
            linky.save()
        except Exception,e:
            response['status'] = 'failed'
            response['error'] = str(e)
            response['traceback'] = traceback.format_exc()
        else:
            response['status'] = 'success'
        return HttpResponse(json.dumps(response), mimetype='application/json')
    else:
        raise NotImplementedError("Must use a POST call for this.")


def removeLink(request):
    """

    """
    response = {}
    if request.method=="POST":
        try:
            l_from = request.POST['from']
            l_to = request.POST['to']
            fromNode = ContentNode.objects.get(name=l_from)
            toNode = ContentNode.objects.get(name=l_to)
            oneWay = Q(pointA=fromNode) & Q(pointB=toNode)
            otherWay = Q(pointA=toNode) & Q(pointB=fromNode)
            links = Link.objects.filter( oneWay | otherWay )
            links.delete()
        except Exception, e:
            response['status']='failed'
            response['error']=str(e)
            response['traceback']=traceback.format_exc()
        else:
            response['status']='success'
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise NotImplementedError("Must use a POST call here.")
            

def fixNodePos(request):
    """
    Let's do a batch thing here to minimize the number of ajax calls we have to make.
    request.POST must contain a list of json decipherable dict things, that contain the
    unique name of a node, and also contain a string describing the "transform(...)"
    coordinate position where we'd like it to be.
    We'll create a gtd position node to store the transform coords, using the unique node
    name and appending some sort of reference as to what type of position it is, or what it's for.
    This name will be guaranteed unique. Then we'll link it to the original node with a linkType
    that's especially for positions. Sound flexible enough?
    """
    response = {}
    if request.method=="POST":
        try:
            nodeList = request.POST['nodeList']
            posNodeType = request.POST['posNodeType']
            posLinkType = request.POST['posLinkType']
            handleFixPos(nodeList, posNodeType, posLinkType)
        except Exception,e:
            response['status']='failed'
            response['error']=str(e)
            response['traceback']=traceback.format_exc()
        else:
            response['status']='success'
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise NotImplementedError("Must use a POST call here")

def handleFixPos(nodeList, pNode_t, pLink_t):
    for item in nodeList:
        nn = ContentNode.objects.get(name=item['nodeName'])
        node_t = NodeType.objects.get(name=pNode_t)
        link_t = LinkType.objects.get(name=pLink_t)
        posStr = item['posStr']
        posNode = ContentNode(name=nn.name+"_"+pNode_t, nodeType=node_t, content=posStr)
        posNode.save()
        posLink = Link(linkType=link_t, pointA=nn, pointB=posNode, direct="b")
        posLink.save()
        

def resetAllNodePos(request):
    """
    This is as simple as deleting each positioned node's position node, and deleting the
    link that used to attach it to that node. On the javascript side some separate thing
    will have to be done to trigger an unpositioning without a page refresh, but perhaps
    a page refresh here wouldn't actually be the worst idea.
    posLinkType in the POST data specifies which links to delete, and nodeLinkType in the
    POST data specifies which 
    """
    response = {}
    if request.method=="POST":
        try:
            posLinkType = request.POST['posLinkType']
        except Exception,e:
            response['status'] = 'failed'
            response['error'] = str(e)
            response['traceback'] = traceback.format_exc()
        else:
            raise NotImplementedError("Must use a POST call here")


def addNode(request):
    """

    """
    pass

def removeNode(request):
    """

    """
    pass
    
def setNodeType(request):
    pass

def filterNodes():
    pass

def filterLinks():
    pass




def getParents(node, *args, **kwargs):
    """
    Retrieve the parent nodes of a given node.
    """
    pass

def getChildren(node, *args, **kwargs):
    """
    Retrieve the children nodes of a given node.
    """

def showMain(request):
    nodes = ContentNode.objects.all()
    links = Link.objects.all()
    return render_to_response('showMain.html', {'nodes':nodes, 'links':links}, context_instance=RequestContext(request))
    
    
def showD3_graph_test(request):
    nodeTypes = NodeType.objects.all()
    linkTypes = LinkType.objects.all()
    return render_to_response('d3Graph.html', {'nodeTypes':nodeTypes, 'linkTypes':linkTypes}, context_instance=RequestContext(request))
