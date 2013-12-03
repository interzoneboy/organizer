from django.contrib import admin
from base.models import ContentNode, Link, NodeType, LinkType

# Register your models here.
admin.site.register(ContentNode)
admin.site.register(Link)
admin.site.register(NodeType)
admin.site.register(LinkType)
