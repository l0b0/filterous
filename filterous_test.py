#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Filterous test suite

Default syntax:

./filterous_test.py
    Run all unit tests
"""

__author__ = 'Victor Engmark'
__email__ = 'victor.engmark@gmail.com'
__url__ = 'http://filterous.sourceforge.net/'
__copyright__ = 'Copyright (C) 2010 Victor Engmark'
__license__ = 'GPLv3'

import unittest

import filterous

class TestValid(unittest.TestCase):
    """Framework for basic tests."""

    def setUp(self):
        """Get XML file contents."""
        # pylint: disable-msg=C0103
        with open('all.xml') as fp:
            self.xml = fp.read()
        self.bookmarks = filterous.Bookmarks(self.xml)

    def tearDown(self):
        """"""
        # pylint: disable-msg=C0103

    def test_empty_tag(self):
        """Empty tag; should not change."""
        self.bookmarks.search(tags = [''])
        self.assertEqual(
            str(self.bookmarks),
            str(filterous.Bookmarks(self.xml)))

    def test_simple_tag(self):
        """Simple tag used in at least one bookmark;
        should not include all the lines from the original."""
        self.bookmarks.search(tags = ['tosee'])
        self.assertNotEqual(
            str(self.bookmarks),
            str(filterous.Bookmarks(self.xml)))

    def test_unused_tag(self):
        """Unused tag; should have no posts left."""
        self.bookmarks.search(tags = ['klaxbar'])
        self.assertEqual(
            len(str(self.bookmarks).splitlines()),
            len(str(filterous.Bookmarks(self.xml)).splitlines()) - 3)

    def test_unicode_tag(self):
        """Unicode tag used in at least one bookmark;
        should not include all the lines from the original."""
        self.bookmarks.search(tags = ['★★★★★'])
        self.assertNotEqual(
            str(self.bookmarks),
            str(filterous.Bookmarks(self.xml)))

    def test_substring_tag(self):
        """Unused tag which is a substring of a used tag; should not change."""
        self.bookmarks.search(tags = ['★'])
        self.assertEqual(
            str(self.bookmarks),
            str(filterous.Bookmarks(self.xml)))

def main():
    """Command line options checkpoint"""
    unittest.main()

if __name__ == '__main__':
    main()
