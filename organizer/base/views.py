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
from base.models import renderEdit, renderAdd, renderView
from django.db.models import Q, Count, Avg
import json
import traceback


# Create your views here.

def getAllNodes_json():
    # ALL of them.
    allNodes = [a.getJson() for a in ContentNode.objects.all()]
    return(allNodes)

def getAllLinks_json():
    # ALL of these also.
    allLinks = [a.getJson() for a in Link.objects.all()]
    return(allLinks)


def getHierarchy_json(rootNodeID, linkType):
    # nodeID is a primary key from the node table, and indicates which node to use as the root
    # for this retrieval. This will return a nested json structure with the given node at the
    # root, and the child nodes under it in a "children" json attribute. Children are found and
    # the structure is populated by following <linkType> links from the root recursively.
    # We attempt to detect loops (which will otherwise cause memory explosions) and perform some
    # sort of logical error behaviour.
    pass

def getGraph(request):
    wahoo = ContentNode.objects.raw("""SELECT cn.id, 
                                              cn.name, 
                                              cn.nodeType_id, 
                                              cn.content, 
                                              ccn.content AS linkcontent,
                                              lt.name AS linktype,
                                              nt.name AS nodetype
                                              FROM base_contentnode cn 
                                              LEFT JOIN base_link ll ON cn.id=ll.pointA_id
                                              AND ll.linktype_id IN (SELECT id from base_linktype WHERE name="gtd_position")
                                              LEFT JOIN base_contentnode ccn ON ll.pointB_id=ccn.id
                                              LEFT JOIN base_linktype lt ON ll.linkType_id=lt.id
                                              LEFT JOIN base_nodetype nt ON cn.nodeType_id=nt.id
                                            
                                              ORDER BY cn.id;""")

    def getjson(x):
        try:
            if x.linktype=="gtd_position":
                return(json.loads(x.linkcontent))
            else:
                return None
        except Exception,e:
            raise
    wahoo2 = [(a, getjson(a)) for a in wahoo]

    def makeJSONstr(tt):
        if tt[1]==None:
            return({'index':tt[0].id, 'origIndex':tt[0].id, 'name':tt[0].name, 'type':tt[0].nodetype})
        elif tt[1]['fixed'] == False:
            return({'index':tt[0].id, 'origIndex':tt[0].id,'name':tt[0].name, 'type':tt[0].nodetype, 'x':tt[1]['x'], 'y':tt[1]['y']})
        elif tt[1]['fixed'] == True:
            return({'index':tt[0].id, 'origIndex':tt[0].id,'name':tt[0].name, 'type':tt[0].nodetype, 'x':tt[1]['x'], 'y':tt[1]['y'], 'fixed':1})
        else:
            raise RuntimeError("What am I doing here")
    def filterNodes(nn):
        if nn[0].nodetype != "gtd_position":
            return(True)
        else:
            return(False)
    
    allLinks = [a for a in Link.objects.exclude(linkType__name='gtd_position')]
    allNodes_dicts = [makeJSONstr(a) for a in wahoo2 if filterNodes(a)==True]
    def calcLinkIndices(ll):
        fromInd = [z['index'] for z in allNodes_dicts].index(ll.pointA_id)
        toInd = [z['index'] for z in allNodes_dicts].index(ll.pointB_id)
        return {'source':fromInd, 'target':toInd}
    
    allLinks_dicts = [calcLinkIndices(a) for a in allLinks]
    retDict = {'nodes':allNodes_dicts, 'links':allLinks_dicts}
    return HttpResponse(json.dumps(retDict), mimetype='application/json')



def getGraph_old(request):
    # Let's just get the graphs nodes, figure out what the indices in the list should be (?), then consult the links
    # and populate a link structure using the indices. The node array and link array must minimally conform to the
    # specifications for a d3 force directed layout.
    # ::TODO:: figure out how the position in the node list affects the layout. Is the first node always the root (eg?)

    # Raw query that lets us get positions and other things from linked nodes.
    


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
                         direct="b",
                         dateCreated=None,
                         dateModified=None)
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
        
def logDecor(fPath):
    def decorator(f):
        def inner(*args, **kwargs):
            with open(fPath, 'w') as logF:
                def innerLog(msg):
                    logF.write(" --- "+msg+"\n")
                    logF.flush()
                kwargs.update({'logger':innerLog})
                logF.write("Calling:  "+str(f)+"\n")
                logF.flush()
                try:
                    return(f(*args, **kwargs))
                except Exception,e:
                    logF.write("Exception from decorator:"+str(e)+"\n")
                    logF.flush()
                    raise
        return inner
    return decorator

class HandleFixPosError(Exception):
    pass
            
            
@logDecor("/tmp/fixNodePos.log")
def fixNodePos(request, **kwargs):
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
    try:
        if request.method=="POST":
            try:
                nodeList = json.loads(request.POST['nodeList'])
                posNodeType = request.POST['posNodeType']
                posLinkType = request.POST['posLinkType']
                handleFixPos(nodeList, posNodeType, posLinkType)
            except:
                kwargs['logger']("3. "+json.dumps(response))
                response['status']='failed'
                response['error']='whoah' #str(e)
                response['traceback']=traceback.format_exc()
            else:
                response['status']='success'

            return HttpResponse(json.dumps(response), mimetype="application/json")
        else:
            kwargs['logger']("What the. "+json.dumps(response))
            raise NotImplementedError("Must use a POST call here")
    except Exception,e:
        kwargs['logger']("whyyyyy")
        raise
@logDecor("/tmp/handleFixPos.log")
def handleFixPos(nodeList, pNode_t, pLink_t, **kwargs):
    kwargs['logger']("NodeList: "+str(nodeList))
    for item in nodeList:
        nn = ContentNode.objects.get(name=item['nodeName'])
        node_t = NodeType.objects.get(name=pNode_t)
        link_t = LinkType.objects.get(name=pLink_t)
        posStrX = item['x']
        posStrY = item['y']
        fixedNess = item['fixed']
        # Get_or_create returns a tuple below. I ALWAYS forget this.
        posNode = ContentNode.objects.get_or_create(name=nn.name+"_"+pNode_t, nodeType=node_t)[0] 
        posNode.content=json.dumps({'fixed':fixedNess,
                                    'x':posStrX,
                                    'y':posStrY})
        posNode.save()
        posLink = Link.objects.get_or_create(linkType=link_t, pointA=nn, pointB=posNode, direct="b")[0]
        posLink.save()
        

@logDecor("/tmp/resetAllNodePos.log")
def resetAllNodePos(request, **kwargs):
    """
    This is as simple as deleting each positioned node's position node, and deleting the
    link that used to attach it to that node. On the javascript side some separate thing
    will have to be done to trigger an unpositioning without a page refresh, but perhaps
    a page refresh here wouldn't actually be the worst idea.
    posLinkType in the POST data specifies which links to delete, and nodeLinkType in the
    POST data specifies which 
    """
    kwargs['logger']("At very beginning.")
    response = {}
    if request.method=="POST":
        try:
            posLinkType = request.POST['posLinkType']
            posNodeType = request.POST['posNodeType']
            lt = LinkType.objects.get(name=posLinkType)
            nt = NodeType.objects.get(name=posNodeType)
            ContentNode.objects.filter(nodeType=nt).delete()
            Link.objects.filter(linkType=lt).delete()
            kwargs['logger']("Finished trying to delete things...")

        except Exception,e:
            kwargs['logger']("in exception clause...")
            response['status'] = 'failed'
            response['error'] = str(e)
            response['traceback'] = traceback.format_exc()
        else:
            kwargs['logger']("in else clause...")
            response['status'] = 'success'

        kwargs['logger']("out of else clause...")
        return HttpResponse(json.dumps(response), mimetype="application/json")
        kwargs['logger']("huh??...")
    else:
        raise NotImplementedError("Must use a POST call here")

@logDecor("/tmp/getNodeEditDiv.log")
def getNodeEditDiv(request, **kwargs):
    response = {}
    if request.method=="POST":
        try:
            nodeName = request.POST['nodeName']
            divHTML = renderEdit(nodeName)
            response['divHtml'] = divHTML
        except Exception,e:
            response['status'] = 'failed'
            response['error'] = str(e)
            response['traceback'] = traceback.format_exc()
        else:
            response['status'] = 'success'
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise NotImplementedError("Must use a POST call here")
        
@logDecor("/tmp/getNodeViewDiv.log")
def getNodeViewDiv(request, **kwargs):
    response = {}
    if request.method=="POST":
        try:
            nodeName = request.POST['nodeName']
            divHTML = renderView(nodeName)
            response['divHtml'] = divHTML
        except Exception,e:
            response['status'] = 'failed'
            response['error'] = str(e)
            response['traceback'] = traceback.format_exc()
        else:
            response['status'] = 'success'
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise NotImplementedError("Must use a POST call here")

def saveNode(request, **kwargs):
    response = {}
    if request.method=="POST":
        try:
            nodeName = request.POST['nodeName']
            nodeTypeName = request.POST['nodeTypeName']
            nodeContent = request.POST['nodeContent']
            cn_pre = ContentNode.objects.get_or_create(name=nodeName)
            cn = cn_pre[0]
            cn_created = cn_pre[1]
            nt = NodeType.objects.get(name=nodeTypeName)
            cn.nodeType = nt
            cn.content = nodeContent
            cn.save()
        except Exception,e:
            response['status'] = 'failed'
            response['error'] = str(e)
            response['traceback'] = traceback.format_exc()
        else:
            response['status'] = 'success'
            response['msg'] = 'created: '+str(cn_created)
            response['nodeContent'] = nodeContent
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise NotImplementedError("Must use a POST call here")

def addNode(request):
    """

    """
    response = {}
    if request.method=="POST":
        try:
            nodeName = request.POST['nodeName']
            nodeTypeName = request.POST['nodeTypeName']
            nt = NodeType.objects.get(name=nodeTypeName)
            nodeContent = request.POST['nodeContent']
            newNode = ContentNode(name=nodeName, nodeType=nt, content=nodeContent, dateCreated=None, dateModified=None)
            newNode.save()
        except Exception,e:
            response['status'] = 'failed'
            response['error'] = str(e)
            response['traceback'] = traceback.format_exc()
        else:
            response['status'] = 'success'
            response['dbIndex'] = newNode.id
            response['dbName'] = newNode.name
            response['dbTypeName'] = newNode.nodeType.name

        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise NotImplementedError("Must use a POST call here")

def orphanNodePurge(*args, **kwargs):
    """
    Nodes can have linked nodes that contain supplementary info, but that shouldn't
    exist on their own, and are usually hidden (like position nodes). When a node and its
    links are deleted, these nodes can be orphaned. 
    This function checks for such orphan nodes and deletes them.
    """
    nodeTypeNames = ['gtd_position']
    query = Q(nodeType__name__in=nodeTypeNames)
    partial = (ContentNode.objects.filter(query).annotate(numALinks = Count('aLinks'))
                                               .annotate(numBLinks = Count('bLinks')))
    full = partial.filter(numALinks=0).filter(numBLinks=0)
    namesDeleted = [a.name for a in full]
    full.delete()
    return namesDeleted
                                                         
    

def deleteNode(request):
    """

    """
    response = {}
    if request.method=="POST":
        try:
            nodeName = request.POST['nodeName']
            node = ContentNode.objects.get(name=nodeName)
            links = Link.objects.filter(Q(pointA=node) | Q(pointB=node))
            linkNames = [(a.pointA.name, a.pointB.name) for a in links]
            response['whichDelete'] = node.name+" "+str(linkNames)
            orphansDeleted = orphanNodePurge()
            response['orphansDeleted'] = orphansDeleted
            node.delete()
            links.delete()
        except Exception,e:
            response['status'] = 'failed'
            response['error'] = str(e)
            response['traceback'] = traceback.format_exc()
        else:
            response['status'] = 'success'
            response['msg'] = 'Node, links, and orphans deleted.'
        return HttpResponse(json.dumps(response), mimetype="application/json")
    else:
        raise NotImplementedError("Must use a POST call here")
    
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
