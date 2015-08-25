# -*- coding: utf-8 -*-

# 导航树指令

"""
目的：动态的生成导航树html
使用方法::

    .. navtree:: asdfasdfasd
       :root_depth: 2

参考： 
http://docutils.sourceforge.net/docs/howto/rst-directives.html

"""
"""
navtree_directive.arguments = (0, 1, 0) 
     three args: required_arguments,optional_arguments,final_argument_whitespace
     .. navtree:: no required_arguments
     :root_depth: one optional_arguments
"""
from docutils import nodes
from docutils.parsers.rst import directives

from zope.component import getMultiAdapter

from zopen.cms.interfaces import INavtreeData, IFRSFolder

from config import nav_root_template, nav_item_template

def navtree_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
    context = state.document.settings.context
    request = state.document.settings.request

    parsed = nav_tree(context, request, options.get('root_depth', 2))
    return [nodes.raw('', parsed, format='html')]

navtree_directive.arguments = (0, 1, 0) 
navtree_directive.has_content = 1
navtree_directive.content = 1  
navtree_directive.options = {'root_depth': int}

directives.register_directive('navtree', navtree_directive)

# 生成navtree
def nav_tree(context, request, root_depth):
    """render navtree structure, root_depth from root"""
    navtree = getMultiAdapter((context,request), INavtreeData)
    if navtree == None:
        return
    # get the root accoding to root_depth
    con = context
    parents = []
    while con.__parent__ != None:
        parents.insert(0,con.__parent__)
        con = con.__parent__

    if IFRSFolder.providedBy(context):
        parents.append(context)
    # 超界
    actual_depth = root_depth
    while actual_depth > len(parents):
        actual_depth -= 1
    root = navtree.singleBranchTree(parents[actual_depth-1])
    # 可能不需要显示
    if root == None:
        return

    root_url = root.get('url')
    root_title = root.get('title')
    tree = root.get('children',[])
    items = []
    dept = 0
    for node in tree:
        items.append(renderNode(node,dept))
        dept += 1
    nav_items = ''.join(items)
    return nav_root_template.substitute(tree=tree,\
                             root_url=root_url,\
                             root_title=root_title,\
                             nav_items=nav_items)

def renderNode(node, dept=0):
    """Supplies node for nav_tree"""
    # 初始化
    class_str = 'node'
    children_str = ''
    icon_str = ''
    a_class_str = ''
    href_mi_icon = '/static/mi.gif'
    href_pl_icon = '/static/pl.gif'

    if node.has_key('flag'):
        if node['flag']=='current':
            class_str += " selected"
            a_class_str += 'navTreeCurrentItem'
    if node['children'] != None and node['children']!=[]:
        class_str += ' loaded expanded'
        icon_str = href_mi_icon
        children_str += """<ul class="navTree navTreeLevel%s">""" % str(dept+1)
        for child_node in node['children']:
            children_str += renderNode(child_node, dept+1)
        children_str += '</ul>'
    elif not node['name'].endswith('.rst'):
        class_str += ' notloaded collapsed'
        icon_str = href_pl_icon

    mi_str = """<img src="%s" border="0" alt="" class="collapseFlag" />""" % href_mi_icon

    pl_str = """<img src="%s" border="0" alt="" class="expandFlag" />""" % href_pl_icon

    if node['children']==None:
        mi_str = ''
        pl_str = ''
    return nav_item_template.substitute(class_str=class_str,
                    node_url=node['url'],
                    mi_str=mi_str,
                    pl_str=pl_str,
                    icon_src=node['icon'],
                    view_name=node.get('view', '/@@view.html'),
                    a_class_str=a_class_str,
                    node_name=node['name'],
                    node_title=node['title'],
                    children_str=children_str
                    )
