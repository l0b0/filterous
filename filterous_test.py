#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Filterous test suite <http://filterous.sourceforge.net/>

Default syntax:

./filterous_test.py
    Run all unit tests
"""

__author__ = 'Victor Engmark'
__email__ = 'victor.engmark@gmail.com'
__copyright__ = 'Copyright (C) 2010 Victor Engmark'
__license__ = 'GPLv3'

from cStringIO import StringIO
import unittest

import filterous

XML = '''<posts tag="" total="3" update="1900-01-01T00:00:00Z" user="none">\n\
  <post \
description="Delicious Command Line Filter" \
extended="" \
hash="f255818ac26a7e0f19c01005630ea3e1" \
href="http://filterous.sourceforge.net/" \
meta="c4ec8ef1570b7c0387b14d7d5f1729cf" \
tag="Delicious CLI search software opensource" \
time="2010-02-09T10:30:15Z" \
/>\n\
  <post description="Example web page description" \
extended="" \
hash="8822003bb3cf9b25b77a2b283944f016" \
href="https://example.org/path/some.file?example=param#fragment" \
meta="a4003e2e2bf880e0d316c31d9de686e1" \
tag="video tosee seen ★★★★★" \
time="2010-02-08T22:46:39Z" \
/>\n\
  <post description="Python Programming Language" \
extended="" \
hash="ff4faae39965af2df932214e2648428d" \
href="http://python.org/" \
meta="54f0fdb28137f2701ddd01c79713e429" \
tag="Python programming language opensource software development reference" \
time="2006-12-01T15:00:52Z" \
/>\n</posts>'''

class TestSearch(unittest.TestCase):
    """Framework for tag AND tests."""
    # pylint: disable-msg=R0904

    def setUp(self):
        """Get XML file contents."""
        # pylint: disable-msg=C0103
        self.xml = StringIO(XML)
        self.result = StringIO()


    def test_empty_tag(self):
        """Empty tag; should get no results."""
        filterous.search(
            self.xml,
            {'tag': [u'']},
            ['href'],
            self.result)
        self.assertEqual(
            self.result.getvalue(),
            '')


    def test_separator_tag(self):
        """Search for tag separator; should get no results."""
        filterous.search(
            self.xml,
            {'tag': [filterous.TAG_SEPARATOR]},
            ['href'],
            self.result)
        self.assertEqual(
            self.result.getvalue(),
            '')


    def test_simple_tag(self):
        """Simple tag used in one bookmark; should get 1 result."""
        filterous.search(
            self.xml,
            {'tag': [u'tosee']},
            ['href'],
            self.result)
        self.assertEqual(
            len(self.result.getvalue().splitlines()),
            1)


    def test_unused_tag(self):
        """Unused tag; should get no results."""
        filterous.search(
            self.xml,
            {'tag': [u'klaxbar']},
            ['href'],
            self.result)
        self.assertEqual(
            self.result.getvalue(),
            '')


    def test_unicode_tag(self):
        """Unicode tag used in one bookmark; should get 1 result."""
        filterous.search(
            self.xml,
            {'tag': [u'★★★★★']},
            ['href'],
            self.result)
        self.assertEqual(
            len(self.result.getvalue().splitlines()),
            1)


    def test_substring_tag(self):
        """Unused tag which is a substring of a used tag;
        should get no results."""
        filterous.search(
            self.xml,
            {'tag': [u'★']},
            ['href'],
            self.result)
        self.assertEqual(
            self.result.getvalue(),
            '')


    def test_empty_tag_not(self):
        """Empty tag; should get N results."""
        filterous.search(
            self.xml,
            {'ntag': [u'']},
            ['href'],
            self.result)
        self.assertEqual(
            len(self.result.getvalue().splitlines()),
            self.xml.getvalue().count('<post '))


    def test_separator_tag_not(self):
        """Search for tag separator; should get N results."""
        filterous.search(
            self.xml,
            {'ntag': [filterous.TAG_SEPARATOR]},
            ['href'],
            self.result)
        self.assertEqual(
            len(self.result.getvalue().splitlines()),
            self.xml.getvalue().count('<post '))


    def test_simple_tag_not(self):
        """Simple tag used in one bookmark; should get N-1 results."""
        filterous.search(
            self.xml,
            {'ntag': [u'tosee']},
            ['href'],
            self.result)
        self.assertEqual(
            len(self.result.getvalue().splitlines()),
            self.xml.getvalue().count('<post ') - 1)


    def test_unused_tag_not(self):
        """Unused tag; should get N results."""
        filterous.search(
            self.xml,
            {'ntag': [u'klaxbar']},
            ['href'],
            self.result)
        self.assertEqual(
            len(self.result.getvalue().splitlines()),
            self.xml.getvalue().count('<post '))


    def test_unicode_tag_not(self):
        """Unicode tag used in one bookmark; should get N-1 results."""
        filterous.search(
            self.xml,
            {'ntag': [u'★★★★★']},
            ['href'],
            self.result)
        self.assertEqual(
            len(self.result.getvalue().splitlines()),
            self.xml.getvalue().count('<post ') - 1)


    def test_substring_tag_not(self):
        """Unused substring of a used tag; should get N results."""
        filterous.search(
            self.xml,
            {'ntag': [u'★']},
            ['href'],
            self.result)
        self.assertEqual(
            len(self.result.getvalue().splitlines()),
            self.xml.getvalue().count('<post '))


    def test_simple_url(self):
        """Domain name match; should get 1 result."""
        filterous.search(
            self.xml,
            {'url': [u'example.org']},
            ['href'],
            self.result)
        self.assertEqual(
            len(self.result.getvalue().splitlines()),
            1)


    def test_empty_url(self):
        """Empty domain name; should get N results."""
        filterous.search(
            self.xml,
            {'url': [u'']},
            ['href'],
            self.result)
        self.assertEqual(
            len(self.result.getvalue().splitlines()),
            self.xml.getvalue().count('<post '))


    def test_simple_url_not(self):
        """Domain name match; should get N-1 results."""
        filterous.search(
            self.xml,
            {'nurl': [u'example.org']},
            ['href'],
            self.result)
        self.assertEqual(
            len(self.result.getvalue().splitlines()),
            self.xml.getvalue().count('<post ') - 1)


    def test_empty_url_not(self):
        """Empty domain name; should get no results."""
        filterous.search(
            self.xml,
            {'nurl': [u'']},
            ['href'],
            self.result)
        self.assertEqual(
            self.result.getvalue(),
            '')


def main():
    """Command line options checkpoint"""
    unittest.main()


if __name__ == '__main__':
    main()
