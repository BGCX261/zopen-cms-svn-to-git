# -*- encoding: utf-8 -*-

from zope.interface import Interface

class IHTMLRenderer(Interface):

    def html():
        """ """

class IFRS(Interface):
    """ ifrs """

class IFRSAsset(Interface):
    """File of the server."""

class IFRSFolder(IFRSAsset):
    """ frs folder """

class IFRSFile(IFRSAsset):
    """ frs folder """

class IFRSDocument(IFRSFile):
    """ frs folder """

class IFRSImage(IFRSFile):
    """ frs folder """

class INavtreeData(Interface):
    """ 一个适配器，获得根据当前上下文对象显示导航树，所需要的数据 """
    def obj2Data(obj):
        """根据对象获取数据"""

    def singleBranchTree(root=''):
        """ 返回当前节点父节点，以及兄弟节点的清单 

        用于显示初始的结构"""

    def children():
        """ 得到当前节点子节点清单

        用于kss action-server调用 """

