##############################################################################
#
# Copyright (c) 2008 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

__version__ = '0.2'

from ez_setup import use_setuptools
use_setuptools()

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'repoze.bfg',
    'Deliverance',
    'zope.structuredtext',
    'zope.security',
    'zopen.frs.core',
    'pygments',
    'kss.base',
    'z3c.batching',
    'DateTime',
    'docutils',
    'zope.traversing',
    'zope.component==3.5.1',
    ]

links = [
    'http://pypi.python.org/pypi/zope.traversing/3.5.0',
    'http://pypi.python.org/pypi/DateTime/2.12.0',
    'http://pypi.python.org/pypi/z3c.batching/1.1.0',
    'http://pypi.python.org/pypi/kss.base/0.3',
    'http://pypi.python.org/pypi/Pygments/1.0',
    'http://pypi.python.org/pypi/zope.security/3.6.2',
    'http://pypi.python.org/pypi/zope.structuredtext/3.4.0',
    'http://pypi.python.org/pypi/Deliverance/0.2.1',
    ]

setup(name='zopen.cms',
      version=__version__,
      description='Serve filesystem content via repoze.bfg',
      long_description=README + '\n\nCHANGES\n\n' + CHANGES,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      keywords='file server wsgi zope',
      author="Agendaless Consulting",
      author_email="zhengping@zopen.cn",
      url="http://zopen.cn",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['zopen'],
      zip_safe=False,
      tests_require = requires,
      install_requires = requires,
      dependency_links = links,
      test_suite="zopen.cms.tests",
      entry_points = """\
      [paste.app_factory]
      app = zopen.cms.run:app
      """,
      )

