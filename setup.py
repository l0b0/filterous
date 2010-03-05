#!/usr/bin/env python
"""Setup configuration."""

from setuptools import setup

setup(
    name = 'Filterous',
    version = '0.7.3',
    description = 'Delicious Command Line Filter',
    author = 'Victor Engmark',
    author_email = 'victor.engmark@gmail.com',
    url = 'http://filterous.sourceforge.net/',
    py_modules = ['filterous'],
    install_requires = ['lxml'],
    test_suite = 'filterous_test',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Topic :: Text Processing :: Filters',])
