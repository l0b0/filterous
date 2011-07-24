#!/usr/bin/env python
"""
Setup configuration
"""

from setuptools import setup
from filterous import filterous as package

setup(
    name=package.__package__,
    version=package.__version__,
    description = 'Delicious Command Line Filter',
    long_description=package.__doc__,
    url=package.__url__,
    keywords = 'Delicious filterous search bookmarks tags',
    packages=[package.__package__],
    install_requires = ['lxml'],
    entry_points={
        'console_scripts': [
            '%(package)s=%(package)s.%(package)s:main' % {
                'package': package.__package__}]},
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
    author=package.__author__,
    author_email=package.__email__,
    maintainer=package.__maintainer__,
    maintainer_email=package.__email__,
    download_url='http://pypi.python.org/pypi/mian/',
    platforms = ['POSIX', 'Windows'],
    license=package.__license__,
    )
