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

    # We sort the list of nodes so the positions correspond to the db ids. We can then use the ids that the links store,
    # and these will refer to the positions in the list that d3 wants to see.
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
        raise NotImplementedError("Must use an ajax call for this.")


def removeLink(request):
    pass

def addNode(request):
    pass

def removeNode(request):
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
