
from base.models import ContentNode, Link, NodeType, LinkType

for nn in ["gtd_realm","gtd_area","gtd_project","gtd_task","gtd_status","gtd_context"]:
    newNode = NodeType(name=nn)
    newNode.save()

def makeGen1(name, gtdType, content="Example Content"):
    nn = ContentNode(name=name, nodeType=NodeType.objects.get(name=gtdType), content=content)
    nn.save()

def makeRealm(name):
    makeGen1(name, "gtd_realm")

def makeArea(name):
    makeGen1(name, "gtd_area")

def makeProject(name):
    makeGen1(name, "gtd_project")

def makeTask(name):
    makeGen1(name, "gtd_task")

def makeStatus(name):
    makeGen1(name, "gtd_status")

def makeContext(name):
    makeGen1(name, "gtd_context")




map(makeRealm, ["Work","Personal","Fantasy"])
map(makeArea, ["Literature","Electronics","MakingProjects","Code","Research","Maintenance","Writing","CAL","Fusion"])
map(makeProject, ["Cal_bayes","fusion_manuscript","fusion_plots","QuantAlgorithmOverhaul","BrowserServerMigration"])
map(makeTask, ["thing"+str(a) for a in range(1,20)])

map(makeStatus, ["task_next","task_future","task_waiting","proj_future","task_urgent","proj_urgent"])
map(makeContext, ["commute", "haulingErrand", "work_focus", "work_tedious", "work_broaden", "distracted"])
