# -*- encoding: utf-8 -*-

import posixpath
from zope.interface import Interface, implements
from zope.component import adapts
from zope.component import queryUtility
from repoze.bfg.interfaces import ISettings

from repoze.bfg.interfaces import IRequest
from repoze.bfg.url import model_url

from interfaces import IFRSAsset, IFRSFolder, IFRSImage, IFRSDocument, IFRSFile, INavtreeData

class NavtreeData(object):
    """ 一个适配器，获得根据当前上下文对象显示导航树，所需要的数据 """

    implements(INavtreeData)
    adapts(IFRSAsset,IRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def singleBranchTree(self, root=''):
        """ 返回当前节点父节点，以及兄弟节点的清单
        用于显示初始的结构"""
        # get Root And Parents
        current = self.context

        nodes = [current] 
        while current.__parent__ != None:
            current = current.__parent__
            nodes.insert(0,current)

        parent_paths = []
        for node in nodes:
            if IFRSFolder.providedBy(node):
                parent_paths.append(node.vpath)
            else:
                break

        if IFRSFile.providedBy(root):
            return self.obj2Data(root.__parent__, parent_paths)

        return self.obj2Data(root, parent_paths)

    def appendChildren(self, root, parent_paths):
        res = []
        if IFRSFolder.providedBy(root):
            for child in root.values(True,True):
                if child.vpath in parent_paths:
                    res.append(self.obj2Data(child, parent_paths))
                else:
                    res.append(self.obj2Data(child))
        return res

    def children(self):
        """ 得到当前节点子节点清单
        用于kss action-server调用 """
        current = self.context
        return [self.obj2Data(child) for child in current.values(True,True)]

    def obj2Data(self, obj, parent_paths=None):
        dc = obj.metadata.get('dublin',{})
        name = obj.__name__
        title = dc.get('title', obj.__name__)
        icon_url = '/static/folder.gif'
        view = '/view.html'

        url = model_url(obj, self.request)
        if IFRSFolder.providedBy(obj):
            view = ''
        else:
            url = url[:-1]

        if IFRSFile.providedBy(obj):
            icon_url = '/static/file.gif'
        if IFRSDocument.providedBy(obj):
            icon_url = '/static/document.gif'
            view = ''
        if IFRSImage.providedBy(obj):
            icon_url = '/static/image.gif'
        data = {
                 'name':name,
                 'url':url,
                 'view':view,
                 'icon':icon_url,
                 'title':title,
                 'children':[],
                 'flag':''
                 }
        if not IFRSFolder.providedBy(obj):
            data['children']=None
        elif parent_paths is not None:
            data['children'] = self.appendChildren(obj, parent_paths)

        if obj.vpath == self.context.vpath:
            data['flag']='current'
        elif obj.vpath + '/index.rst' == self.context.vpath:
            for child in data['children']:
                if 'index.rst' == data['name']:
                    return data
            data['flag']='current'
        return data
