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
    allLinks_dicts = [{'source':a.pointA_id, 'target':a.pointB_id} for a in allLinks]
    retDict = {'nodes':allNodes_dicts, 'links':allLinks_dicts}
    return HttpResponse(json.dumps(retDict), mimetype='application/json')

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
    return render_to_response('d3Graph.html', {}, context_instance=RequestContext(request))
