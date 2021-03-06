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
        'repoze.bfg==0.6.8',
    ]

links = [
    ]

setup(name='demosite',
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
      keywords='file server wsgi zope demosite',
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
      test_suite="demosite.tests",
      entry_points = """
      """,
      )

