#!/usr/bin/env python
"""
Setup configuration
"""

from setuptools import find_packages, setup
from filterous.filterous import __doc__ as module_doc

setup(
    name = 'Filterous',
    version = '0.8.2',
    description = 'Delicious Command Line Filter',
    long_description = module_doc,
    url = 'http://filterous.sourceforge.net/',
    keywords = 'Delicious filterous search bookmarks tags',
    packages = find_packages(exclude=['tests']),
    install_requires = ['lxml'],
    entry_points = {
        'console_scripts': ['filterous = filterous.filterous:main']},
    classifiers = [
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
    maintainer = 'Victor Engmark',
    maintainer_email = 'victor.engmark@gmail.com',
    download_url = 'http://sourceforge.net/projects/filterous/files/',
    platforms = ['POSIX', 'Windows'],
    license = 'GPL v3 or newer',
    )
