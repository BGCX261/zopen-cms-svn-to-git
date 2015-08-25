# -*- coding: utf-8 -*-

# docutilis一组补丁集合
import docutilsplugins

# 让Deliverance支持中文

from deliverance.wsgimiddleware import DeliveranceMiddleware
#from deliverance.middleware import DeliveranceMiddleware
old_filter_body = DeliveranceMiddleware.filter_body

def filter_body(self, environ, orig_environ, body):
    body = body.decode('utf-8')
    return old_filter_body(self, environ, orig_environ, body)

DeliveranceMiddleware.filter_body = filter_body
