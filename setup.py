# -*- coding: utf-8 -*-
"""
This module contains the tool of plonesocial.auth.rpx
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.815'

long_description = (
    read('docs', 'README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('docs', 'CHANGES.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

tests_require=['zope.testing']

setup(name='plonesocial.auth.rpx',
      version=version,
      description="An RPX connector for Plone, allowing users to login with Twitter, Google, Facebook etc.",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Zope2',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management',

        ],
      keywords='rpx plone google twitter openid facebook yahoo janrain login identity identification authentication cms',
      author='Carsten Rebbien, Christian Scholz (COM.lounge GmbH)',
      author_email='cr@comlounge.net',
      url='http://comlounge.net/rpx/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plonesocial', 'plonesocial.auth'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        'simplejson',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'plonesocial.auth.rpx.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*- 
      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      
      [z3c.autoinclude.plugin]
      target = plone
      """,
      paster_plugins = ["ZopeSkel"],
      )
