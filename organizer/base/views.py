# The view functions described here are the "api" or more accurately the interface
# through which the database storage and data persistence will be done. The functions
# in this model will return Nodes, Links, and Graphs (as lists) for use in html templates,
# d3/other js, and anywhere else.
#
# [a for a in ...] comprehension structure is used so that actual lists of objects are returned
# from these functions, not unexecuted django querysets.
#
from django.shortcuts import render
from base.models import ContentNode, NodeType
from base.models import Link, LinkType


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

def filterNodes(...):
    pass

def filterLinks(...):
    pass
