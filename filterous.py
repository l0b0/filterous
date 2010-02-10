#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Filterous - Delicious Command Line Filter

Default syntax:

./filterous.py < all.xml

Options:
--tag      Tag search string (@tag)
--ntag     Negated tag search string (@tag)
--desc     Description search string (@description)
--ndesc    Negated description search string (@description)
--note     Note search string (@extended)
--nnote    Negated note search string (@extended)
--url      URL search string (@href)
--nurl     Negated URL search string (@href)

Description:
Will search the tags of the XML file downloaded from
<https://api.del.icio.us/v1/posts/all>. To avoid the slow load of that page in
a web browser, you can use one of the following commands:

curl -ku username:password https://api.del.icio.us/v1/posts/all

wget --no-check-certificate --user=username --password=password -O all.xml \
https://api.del.icio.us/v1/posts/all

Examples:

./filterous.py --tag=video --tag=tosee --ntag=seen < all.xml
    Returns links to unseen videos.

./filterous.py --nurl=^https < all.xml
    Returns non-HTTPS links.

./filterous.py --ntag=^for: --tag=★★★★★ < all.xml
    Returns great links that you have not shared with your contacts.
"""

__author__ = 'Victor Engmark'
__email__ = 'victor.engmark@gmail.com'
__url__ = 'http://filterous.sourceforge.net/'
__copyright__ = 'Copyright (C) 2010 Victor Engmark'
__license__ = 'GPLv3'

import xml.etree.ElementTree as ET

TAG_SEPARATOR = u' '

class DeliciousBookmarks(ET.ElementTree):
    """Has a list of bookmarks with their metadata and display functions."""

    def search_tags_and(self, tags):
        """
        Check that all tags are present. Remove the bookmark if not.

        @param tags: List of tags
        """
        root = self.getroot()
        bookmarks = root.getchildren()
        garbage = []
        for tag in tags:
            for bookmark in bookmarks:
                if tag not in bookmark.attrib['tag'].split(TAG_SEPARATOR):
                    garbage.append(bookmark)

        for bookmark in garbage:
            root.remove(bookmark)

    def search_tags_not(self, tags):
        """
        Check that no tags are present. Remove the bookmark if they are.

        @param tags: List of tags
        """
        root = self.getroot()
        bookmarks = root.getchildren()
        garbage = []
        for tag in tags:
            for bookmark in bookmarks:
                if tag in bookmark.attrib['tag'].split(TAG_SEPARATOR):
                    garbage.append(bookmark)

        for bookmark in garbage:
            root.remove(bookmark)

    def search_url(self, url):
        """
        URL substring match.

        @param url: Substring of an URL
        """
        root = self.getroot()
        bookmarks = root.getchildren()
        garbage = []
        for bookmark in bookmarks:
            if bookmark.attrib['href'].find(url) == -1:
                garbage.append(bookmark)

        for bookmark in garbage:
            root.remove(bookmark)

    def search(
        self,
        tags = None,
        ntags = None,
        desc = None,
        ndesc = None,
        note = None,
        nnote = None,
        url = None,
        nurl = None,
        etags = None,
        edesc = None,
        enote = None,
        eurl = None):
        """
        Find matching bookmarks.

        @param search: List of tag regexes to match
        """

        if tags is not None:
            self.search_tags_and(tags)

        if ntags is not None:
            self.search_tags_not(ntags)

        if url is not None:
            self.search_url(url)
