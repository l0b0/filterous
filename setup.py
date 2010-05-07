#!/usr/bin/env python
"""
Setup configuration

Prerequisites: libxml2-dev and libxslt-dev
"""

from setuptools import find_packages, setup
from filterous import __doc__ as fdoc

setup(
    name = 'Filterous',
    version = '0.8',
    description = 'Delicious Command Line Filter',
    url = 'http://filterous.sourceforge.net/',
    long_description = fdoc,
    keywords = 'Delicious filterous search bookmarks tags',
    packages = find_packages(exclude=['tests']),
    install_requires = ['lxml'],
    entry_points = {'console_scripts': ['filterous = filterous.filterous:main']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Topic :: Text Processing :: Filters',
    ],
    test_suite = 'tests.tests',
    author = 'Victor Engmark',
    author_email = 'victor.engmark@gmail.com',
    )
