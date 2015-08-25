# -*- encoding: UTF-8 -*-
from zope.interface import implements
from zope.component import adapts

from interfaces import IFRSDocument, IHTMLRenderer

import docutils.core
from docutils.writers.html4css1 import HTMLTranslator, Writer

class Document:
    implements(IHTMLRenderer)
    adapts(IFRSDocument)

    def __init__(self, file):
        self.file = file

    def html(self):
        data = self.file.data
        # XXX html?
        lstrip_data = data.lstrip()
        if lstrip_data and lstrip_data[0] == '<':
            return data

        # see : http://docutils.sourceforge.net/docs/user/config.html
        settings = {
            'halt_level': 6,
            'input_encoding':'UTF-8',
            'output_encoding':'UTF-8',
            'initial_header_level' : 2,
            'file_insertion_enabled' : 1,
            'raw_enabled' : 1,
            'writer_name':'html',
            'language_code':'zh_cn'
            }

        ospath = self.file.ospath

        # windows会自动增加utf8的标识字
        if lstrip_data[0:3]== '\xef\xbb\xbf':
            lstrip_data = lstrip_data[3:]

        # 不显示的标题区域，标题在zpt里面独立处理了
        if lstrip_data.startswith('======'):
            splitted_data = lstrip_data.split('\n', 3)
            data = splitted_data[-1]
            #title = splitted_data[1]

        # 表格生成的时候，会出现一个border=1，需要去除
        data = data.replace('border="1"', '')
        html_content = docutils.core.publish_parts(
            data,
            source_path = str(ospath),
            writer=Writer(),
            settings_overrides=settings,) ['html_body']
        return html_content
