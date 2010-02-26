#!/usr/bin/env python
"""Setup configuration."""

from setuptools import setup

setup(
    name = 'Filterous',
    version = '0.7',
    description = 'Delicious Command Line Filter',
    author = 'Victor Engmark',
    author_email = 'victor.engmark@gmail.com',
    url = 'http://vcard-module.sourceforge.net/',
    py_modules = ['filterous'],
    install_requires = ['lxml'],
    test_suite = 'filterous_test',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Intended Audience :: End Users/Desktop',
        'Development Status :: 4 - Beta',
        'Topic :: Text Processing :: Filters',
        'Programming Language :: Python :: 2.6',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Natural Language :: English'])
