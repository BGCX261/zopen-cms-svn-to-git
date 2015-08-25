#coding=utf-8

import os

from webob import Response

from zope.component import getMultiAdapter

from kss.base.commands import KSSCommands
from kss.base.corecommands import KSSCoreCommands
from kss.base.selectors import *

from selectors import parentnodecss

from interfaces import INavtreeData

from config import navitem_template

### KSSVIEW ###

def showChildren(context, request):
    node_obj = context
    current_node = getMultiAdapter((node_obj, request),INavtreeData)\
            .obj2Data(node_obj)

    children =getMultiAdapter((node_obj, request),INavtreeData).children()
    
    children_str=''
    mi_str = """ <img src="/static/mi.gif" border="0" alt="" class="collapseFlag" /> """
    pl_str = """ <img src="/static/pl.gif" border="0" alt="" class="expandFlag" /> """

    for node in children:
        _mi_str = mi_str
        _pl_str = pl_str
        if node['children'] == None:
            _mi_str = ''
            _pl_str = ''

        children_str += navitem_template.substitute(class_str='notloaded collapsed',\
                node_url=node['url'], a_class_str='',\
                view_name=node.get('view', '/@@view.html'),\
                mi_str=_mi_str,pl_str=_pl_str,\
                icon_src=node['icon'], node_name=node['name'], \
                node_title=node['title'],children_str='')

    children_text = """
           <ul class="navTree navTreeLevel2">
               %s
           </ul>
           """ % children_str

    content= navitem_template.substitute(class_str='loaded expanded',
                    node_url=current_node['url'],
                    a_class_str='',
                    mi_str=mi_str,
                    view_name=current_node.get('view', '/@@view.html'),
                    pl_str=pl_str, 
                    icon_src=current_node['icon'],
                    node_name=current_node['name'],
                    node_title=current_node['title'],
                    children_str=children_text)

    commands = KSSCommands()
    core=KSSCoreCommands(commands)
    core.replaceHTML(parentnodecss('li.navTreeItem|'),content)
    return Response(commands.render(), content_type='text/xml')

