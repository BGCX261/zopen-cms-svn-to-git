# -*- encoding: utf-8 -*-

from repoze.bfg.router import make_app
from repoze.bfg.settings import get_options

from zope.component import getUtility
from zope.component import getGlobalSiteManager

from zopen.frs.core import FRS
from interfaces import IFRS
from model import Folder

import os

mount_paths = []

def initFRS(event):
    frs = getUtility(IFRS)
    for root in mount_paths:
        mount_name = os.path.basename(root) or os.path.basename(root[:-1])
        frs.mount(mount_name, root)

def app(global_config, roots=None, root_vpath='/', **kw):
    import zopen.cms

    if roots is None:
        raise ValueError('zopen.cms requires a roots')

    for root in roots.split(';'):
        root = root.strip()
        mount_paths.append(root)


    # 根据配置，初始化文件库
    folder = Folder()
    folder.__parent__ = None
    folder.__name__ = ''
    folder.vpath = root_vpath

    def get_root(environ):
        return folder
 
    return make_app(get_root, zopen.cms, options=kw)

