# -*- encoding: utf-8 -*-

import os, tempfile
import datetime
import time

from repoze.bfg.chameleon_zpt import render_template_to_response
from repoze.bfg.interfaces import ISettings

from zope.component import queryUtility
from zope.traversing.browser import absoluteURL
from z3c.batching.batch import Batch
from webob.exc import HTTPFound

from interfaces import IHTMLRenderer
from interfaces import IFRSFolder, IFRSDocument
from views import render_tabs, render_cols
from batch_views import batch_view as render_batch
from utils import getDisplayTime

def blog_view(context, request):
    batch_start = int(request.params.get('b_start', 0))
    posts = []
    blog_subpaths = context.get_recent_file_subpaths()
    if batch_start >= len(blog_subpaths):
        return HTTPFound(location=request.url.split('?b_start')[0])

    for subpath in blog_subpaths:
        obj = context.get_obj_by_subpath(subpath)
        if obj != None:
            url = '/'.join(obj.vpath.split('/')[2:])
            dc = obj.metadata.get('dublin', {})
            raw_html = IHTMLRenderer(obj).html().decode('utf-8')
            converted_html = raw_html.replace('src="img/',\
                         'src="%s/%s/../img/' %(request.application_url, url))
            posts.append( {'title':dc.get('title', obj.__name__),
                           'description':dc.get('description', ''),
                           'url':'/'.join(url.split('/')[1:]),
                           'created':getDisplayTime(dc.get('created', '')),
                           'creator':dc.get('creators', [])[0],
                           'body': converted_html[:500]+' ......',
                           })

    posts = Batch(posts, start=batch_start, size=5)
    
    dc = context.metadata.get('dublin', {})
    tabs = render_tabs(context,request)
    html_cols = render_cols(context, request)
    batch = render_batch(context, request)
    return render_template_to_response('templates/blog.pt',
            title = dc.get('title', context.__name__),
            result = posts,
            tabs = tabs,
            batch = batch,
            html_cols = html_cols,
            )

def blog_post_view(context, request):
    result = {}
    obj = context
    dc = obj.metadata.get('dublin',{})
    result['title'] = dc.get('title', obj.__name__)
    result['description'] = dc.get('description', '')
    result['url'] = obj.__name__
    result['created'] = dc.get('created', '')
    result['creator'] = dc.get('creators', [])[0]

    pachs = request.url.split('/')
    img_url =  '/'.join(pachs[0:len(pachs)-2]) + '/img/'

    result['body'] = IHTMLRenderer(obj).html().replace('src="img/', 'src="%s' % img_url)
    tabs = render_tabs(context,request)

    settings = queryUtility(ISettings)
    idcomments_acct = str(getattr(settings, 'idcomments_acct', ''))
    return render_template_to_response('templates/blogpost.pt',
            title = dc.get('title', context.__name__),
            result = result,
            tabs = tabs,
            post_created = getDisplayTime(result['created']),
            idcomments_acct = idcomments_acct,
            )
