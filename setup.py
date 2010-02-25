#!/usr/bin/env python
"""Setup configuration."""

from distutils.core import setup

setup(
    name = 'Filterous',
    version = '0.6.2',
    description = 'Delicious Command Line Filter',
    author = 'Victor Engmark',
    author_email = 'victor.engmark@gmail.com',
    url = 'http://vcard-module.sourceforge.net/',
    py_modules = ['filterous'],
    install_requires = ['lxml'],
    test_suite = 'filterous_test')
