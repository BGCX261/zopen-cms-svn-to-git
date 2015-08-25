# -*- encoding: utf-8 -*-

import os
import mimetypes

import smtplib
from email import MIMEText
from email import Header

import docutils.core
from docutils.writers.html4css1 import Writer

from repoze.bfg.chameleon_zpt import render_template_to_response
from repoze.bfg.chameleon_zpt import render_template
from repoze.bfg.push import pushpage
from repoze.bfg.interfaces import IView
from repoze.bfg.view import static
from repoze.bfg.settings import get_options
from repoze.bfg.interfaces import ISettings

from zope.component import queryUtility
from zope.component import getUtility

from webob import Response
from webob.exc import HTTPFound

from interfaces import IHTMLRenderer
from interfaces import IFRSFolder, IFRSDocument

#mimetypes.add_type('text/html', '.py')
#mimetypes.add_type('text/html', '.zcml')
#mimetypes.add_type('application/pdf', '.pdf')

resources_view = static('resources')
rules_view = static('deliverance/rules')
static_view = static('templates/static')

def folder_view(context, request):
    if not request.url.endswith('/'):
        response = HTTPFound(location=request.url + '/')
        return response

    defaults = ('index.html', 'index.rst')
    for name in defaults:
        try:
            index = context[name]
        except KeyError:
            continue
        return document_view(index, request)

    contents = []
    for obj in context.values(True, True):
        dc = obj.metadata.get('dublin', {})

        if hasattr(obj, '__getitem__'):
            url = obj.__name__ + '/'
        else:
            url = obj.__name__
        contents.append({'name':obj.__name__,
                        'title':dc.get('title', ''),
                        'url':url,
                        'description':dc.get('description', '')})

    dc = context.metadata.get('dublin', {})

    tabs = render_tabs(context,request)
    html_cols = render_cols(context, request)
    return  render_template_to_response('templates/contents.pt',
             title = dc.get('title', context.__name__),
             description = dc.get('description', ''),
             contents = contents,
             html_cols = html_cols,
             tabs = tabs,)

def render_tabs(context, request):
    cur_path = request.path
    res = '<ul id="portal-globalnav"> '
    settings = queryUtility(ISettings)
    class_str = 'plain'
    tabs = eval(getattr(settings, 'tabs', '[]'))
    selected_flag = False
    tab_list = []
    tmp_tabs = tabs[:]

    def my_cmp(E1, E2):
        return -cmp(E1[-1], E2[-1])
    if tmp_tabs != '' or []:
        tmp_tabs.sort(my_cmp)

    for tab in tmp_tabs:
        class_str = 'plain'
        tab_id ,tab_url, tab_path = tab[0], tab[1], tab[-1]
        
        if cur_path.startswith(tab_path) and selected_flag == False:
            class_str = "selected"
            selected_flag = True
        
        html_str = """<li id="%s" class="%s">
                        <a href="%s">%s</a>
                      </li>""" %(tab_id, class_str, tab_url,tab_id)
        tab_list.append((tab_url, html_str))

    for tab in tabs:
        for tab1 in tab_list:
            if tab[1] == tab1[0]:
                res = res + tab1[1]
    res = res + '</ul>'
    return res.decode('utf-8')

def rst_col_path(name, context):
    # 往上找左右列
    if context.__name__ == '':
        return '',''
    source_path = str(context.ospath)
    if IFRSFolder.providedBy(context):
        source_path = os.path.join(source_path, 'asf.rst')
    dc_main = context.metadata.get('main', {})
    col = dc_main.get(name, '')
    if col != '':
        return col, source_path
    if context.__parent__ == None: 
        return col, source_path
    return rst_col_path(name, context.__parent__)

def rst2html(rst, path, context, request):
    lstrip_rst = rst.lstrip()
    if lstrip_rst and lstrip_rst[0] == '<':
        return rst

    settings = {
        'halt_level': 6,
        'input_encoding':'UTF-8',
        'output_encoding':'UTF-8',
        'initial_header_level' : 2,
        'file_insertion_enabled' : 1,
        'raw_enabled' : 1,
        'writer_name':'html',
        'language_code':'zh_cn',
        'context':context,
        'request':request
        }

    # 表格生成的时候，会出现一个border=1，需要去除
    rst = rst.replace('border="1"', '')
    html_content = docutils.core.publish_parts(
            rst,
            source_path = path,
            writer=Writer(),
            settings_overrides=settings,) ['html_body']

    return html_content

def render_cols(context, request):
    html_left = ''
    html_right = ''
    right_col_rst, right_col_path = rst_col_path('right_col', context)
    left_col_rst, left_col_path = rst_col_path('left_col', context)
    center_col_rst, center_col_path = rst_col_path('center_col', context)

    if left_col_rst == '':
        html_left = ''
    else:
        cvt_html = rst2html(left_col_rst, left_col_path, context, request)
        if cvt_html.startswith('<td') or cvt_html.lstrip().startswith('<td'):
            html_left = cvt_html
        else:
            html_left = """<td id="portal-column-one">
            <div class="visualPadding"> %s </div> </td> 
            """ % rst2html(left_col_rst, left_col_path, context, request)

    if right_col_rst == '':
        html_right = ''
    else:
        cvt_html = rst2html(right_col_rst, right_col_path, context, request)
        if cvt_html.startswith('<td') or cvt_html.lstrip().startswith('<td'):
            html_right = cvt_html
        else:
            html_right = """<td id="portal-column-two">
            <div class="visualPadding"> %s </div> </td> 
            """ % rst2html(right_col_rst, right_col_path, context, request)

    if center_col_rst == '':
        html_center = ''
    else:
        cvt_html = rst2html(center_col_rst, center_col_path, context, request)
        html_center = """ <div> %s </div> 
        """ % rst2html(center_col_rst, center_col_path, context, request)

    html_cols = {'left': html_left,
                 'right': html_right,
                 'center': html_center, 
                 }
    return html_cols

def document_view(context, request):
    html = IHTMLRenderer(context).html()
    html_cols = render_cols(context, request)

    settings = queryUtility(ISettings)
    site_title = getattr(settings, 'site_title', '').decode('utf-8')

    dc = context.metadata.get('dublin', {})
    tabs = render_tabs(context,request)
    return render_template_to_response('templates/document.pt',
            title = dc.get('title', context.__name__),
            description = dc.get('description', ''),
            site_title = site_title,
            html = html,
            tabs = tabs,
            html_cols = html_cols, 
            )

def file_view(context, request):
    dc = context.metadata.get('dublin', {})
    tabs = render_tabs(context,request)
    return render_template_to_response('templates/file.pt',
             title = dc.get('title', context.__name__),
             description = dc.get('description', ''),
            url=context.__name__,
            tabs = tabs,
            )

def image_view(context, request):
    dc = context.metadata.get('dublin', {})
    tabs = render_tabs(context,request)
    return render_template_to_response('templates/image.pt',
             title = dc.get('title', context.__name__),
             description = dc.get('description', ''),
            url=context.__name__,
            tabs = tabs,
            )

def rss_view(context, request):
    return render_template_to_response('templates/rss.pt',
               request = request,
            )

def download_view(context, request):
    response = Response(context.data)
    filename = context.frs.basename(context.vpath)
    mt, encoding = mimetypes.guess_type(filename)
    response.content_type = mt or 'text/plain'
    return response


def contact_view(context, request):
    params = request.params
    reply_str = ''
    sender_fullname = params.get('sender_fullname', '')
    sender_from_address = params.get('sender_from_address', '')
    company_name = params.get('company_name', '')
    company_website = params.get('company_website', '')
    company_tel = params.get('company_tel', '')
    subject = params.get('subject', '')
    message = params.get('message', '')

#    if sender_from_address!='' and company_name!=''\
#         and company_tel!='' and subject!='' and message!='':
    if sender_from_address!='' and subject!='' and message!='':

        body = """%s 消息回馈:
回馈人信息：
NAME: %s
EMAIL: %s
COMPANY NAME: %s
COMPANY WEBSITE: %s
COMPANY TEL: %s

SUBJECT: %s
CONTENT: 
%s
                 """ % (request.application_url, sender_fullname, \
                        sender_from_address, company_name, company_website, \
                        company_tel, subject, message)

        settings = queryUtility(ISettings)
        smtp_host = getattr(settings, 'smtp_host', '')
        from_addr = getattr(settings, 'email_from', '')
        user_name = getattr(settings, 'user_name', '')
        user_passwd = getattr(settings, 'user_passwd', '')
        to_addr = getattr(settings, 'email_to', '')
        
        """邮件参数
        smtp_host = smtp.***.com
        email_from = usr1@***.com
        email_to = usr2@***.com
        user_name = 'usr1'
        user_passwd = '123*'
        """
        try:
            """
            msg = MIMEText.MIMEText(body,_subtype='plain',_charset='utf-8')
            msg['subject'] = Header.Header(subject,'utf-8')
            msg['from'] = from_addr  
            msg['to'] = to_addr  
            """
            msg = 'to: %s\r\nFrom: %s\r\nSubject: %s \r\n\r\n %s\r\n' \
                                 %(to_addr, from_addr, subject, body)
            server = smtplib.SMTP(smtp_host,25)
            server.ehlo()
            server.starttls()
            server.ehlo() 
            server.login(user_name, user_passwd) 
            server.sendmail(from_addr,to_addr,msg)
            server.close()

            reply_str = '信息已经发出，谢谢。'
            sender_fullname = ''
            sender_from_address = ''
            company_name = ''
            company_website = ''
            company_tel = ''
            subject = ''
            message = ''
        except:
            reply_str = '邮件收发设置信息错误。请稍后重试，或通过其他方式反馈。'
    else:
        reply_str = '必填项信息不足，请补全。'

    return render_template_to_response('templates/contact.pt',
                            reply_str = reply_str.decode('utf-8'),
                            sender_fullname = sender_fullname.decode('utf-8'),
                            sender_from_address = sender_from_address.decode('utf-8'),
                            company_name = company_name.decode('utf-8'),
                            company_website = company_website.decode('utf-8'),
                            company_tel = company_tel.decode('utf-8'),
                            subject = subject.decode('utf-8'),
                            message = message.decode('utf-8'),
                            )

