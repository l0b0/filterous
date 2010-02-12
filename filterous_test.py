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

try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree
                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")
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

def _posts(bookmarks):
    """Element objects for each post"""
    return bookmarks.getroot().getchildren()

class TestRegex(unittest.TestCase):
    """Framework for testing regular expression generators."""

    def test_format_simple(self):
        """Simple formatting XPath"""
        xp = filterous.get_format_xpath(['tag'])
        expected = '@tag'
        self.assertNotEqual(xp, None)
        self.assertEqual(xp.path, expected)


    def test_search_simple(self):
        """Simple search XPath"""
        xp = filterous.get_search_xpath({'tag': ['foobar']})
        expected = "/posts/post[contains(\
concat(' ', @tag, ' '), \
concat(' ', 'foobar', ' '))]"
        self.assertNotEqual(xp, None)
        self.assertEqual(xp.path, expected)


    def test_search_complex(self):
        """Complex search XPath"""
        xp = filterous.get_search_xpath({
            'tag': ['foo&bar', 'na"lle'],
            'url': ['https://', 'example.org'],
            'note': ['<test>', "'fisk'", 'æé€']
            })
        expected = ""
        self.assertNotEqual(xp, None)
        self.assertEqual(xp.path, expected)


class TestAll(unittest.TestCase):
    """Framework for tag AND tests."""
    # pylint: disable-msg=R0904

    def setUp(self):
        """Get XML file contents."""
        # pylint: disable-msg=C0103
        self.bookmarks = filterous.DeliciousBookmarks(
            ET.fromstring(XML))


    def test_empty_tag(self):
        """Empty tag; should have no posts left."""
        self.bookmarks.search({'tag': [u'']})
        self.assertEqual(
            _posts(self.bookmarks),
            [])


    def test_separator_tag(self):
        """Search for tag separator; should have no posts left."""
        self.bookmarks.search({'tag': [filterous.TAG_SEPARATOR]})
        self.assertEqual(
            _posts(self.bookmarks),
            [])


    def test_simple_tag(self):
        """Simple tag used in one bookmark; should have 1 post left."""
        self.bookmarks.search({'tag': [u'tosee']})
        self.assertEqual(
            len(_posts(self.bookmarks)),
            1)


    def test_unused_tag(self):
        """Unused tag; should have no posts left."""
        self.bookmarks.search({'tag': [u'klaxbar']})
        self.assertEqual(
            _posts(self.bookmarks),
            [])


    def test_unicode_tag(self):
        """Unicode tag used in one bookmark; should have 1 post left."""
        self.bookmarks.search({'tag': [u'★★★★★']})
        self.assertEqual(
            len(_posts(self.bookmarks)),
            1)


    def test_substring_tag(self):
        """Unused tag which is a substring of a used tag;
        should have no posts left."""
        self.bookmarks.search({'tag': [u'★']})
        self.assertEqual(
            _posts(self.bookmarks),
            [])

    def test_empty_tag_not(self):
        """Empty tag; should not change."""
        self.bookmarks.search({'ntag': [u'']})
        self.assertEqual(
            ET.tostring(self.bookmarks.getroot(), 'utf-8'),
            XML)


    def test_separator_tag_not(self):
        """Search for tag separator; should not change."""
        self.bookmarks.search({'ntag': [filterous.TAG_SEPARATOR]})
        self.assertEqual(
            ET.tostring(self.bookmarks.getroot(), 'utf-8'),
            XML)


    def test_simple_tag_not(self):
        """Simple tag used in one bookmark; should have N-1 posts left."""
        self.bookmarks.search({'ntag': [u'tosee']})
        self.assertEqual(
            len(ET.tostring(self.bookmarks.getroot(), 'utf-8').splitlines()),
            len(XML.splitlines()) - 1)


    def test_unused_tag_not(self):
        """Unused tag; should not change."""
        self.bookmarks.search({'ntag': [u'klaxbar']})
        self.assertEqual(
            ET.tostring(self.bookmarks.getroot(), 'utf-8'),
            XML)


    def test_unicode_tag_not(self):
        """Unicode tag used in one bookmark; should have N-1 posts left."""
        self.bookmarks.search({'ntag': [u'★★★★★']})
        self.assertEqual(
            len(ET.tostring(self.bookmarks.getroot(), 'utf-8').splitlines()),
            len(XML.splitlines()) - 1)


    def test_substring_tag_not(self):
        """Unused tag which is a substring of a used tag; should not change."""
        self.bookmarks.search({'ntag': [u'★']})
        self.assertEqual(
            ET.tostring(self.bookmarks.getroot(), 'utf-8'),
            XML)

    def test_simple_url(self):
        """Domain name match"""
        self.bookmarks.search({'url': [u'example.org']})
        self.assertEqual(
            len(_posts(self.bookmarks)),
            1)

def main():
    """Command line options checkpoint"""
    unittest.main()


if __name__ == '__main__':
    main()
