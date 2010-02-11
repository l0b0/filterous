#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Filterous - Delicious Command Line Filter

Default syntax:

./filterous.py [options] < all.xml

Options:
--tag      Tag search string (@tag)
--ntag     Negated tag search string (@tag)
--desc     Description search string (@description)
--ndesc    Negated description search string (@description)
--note     Note search string (@extended)
--nnote    Negated note search string (@extended)
--url      URL search string (@href)
--nurl     Negated URL search string (@href)
-t         Show tags
-d         Show descriptions
-n         Show notes

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

import getopt
import sys
import xml.etree.ElementTree as ET

TAG_SEPARATOR = u' '

class DeliciousBookmarks(ET.ElementTree):
    """Has a list of bookmarks with their metadata and display functions."""

    def pretty_print(
        self,
        show_tags = False,
        show_descriptions = False,
        show_notes = False):
        """Print shell output, optionally with tags, descriptions and notes."""
        lines = []

        for post in self.getroot().getchildren():
            lines.append(post.get('href'))

            if show_tags:
                lines.append(post.get('tag'))

            if show_descriptions:
                lines.append(post.get('description'))

            if show_notes:
                lines.append(post.get('extended'))

            if show_tags or show_descriptions or show_notes:
                # Space the posts nicely
                lines.append('')

        return '\n'.join(lines)


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
                if tag not in bookmark.attrib['tag'].split(TAG_SEPARATOR) and \
                       bookmark not in garbage:
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
                if tag in bookmark.attrib['tag'].split(TAG_SEPARATOR) and \
                       bookmark not in garbage:
                    garbage.append(bookmark)

        for bookmark in garbage:
            root.remove(bookmark)


    def search_url(self, urls):
        """
        URL substring match.

        @param url: Substring of an URL
        """
        root = self.getroot()
        bookmarks = root.getchildren()
        garbage = []
        for url in urls:
            for bookmark in bookmarks:
                if bookmark.attrib['href'].find(url) == -1 and \
                       bookmark not in garbage:
                    garbage.append(bookmark)

        for bookmark in garbage:
            root.remove(bookmark)


    def search(
        self,
        search):
        """
        Remove posts that don't match the search terms.

        @param search: Dictionary of search terms.
        """

        if 'tag' in search:
            self.search_tags_and(search['tag'])
        if 'ntag' in search:
            self.search_tags_not(search['ntag'])
        if 'url' in search:
            self.search_url(search['url'])


class Usage(Exception):
    """Raise in case of invalid parameters."""
    # pylint: disable-msg=W0231
    def __init__(self, msg):
        self.msg = msg


def main(argv = None):
    """Argument handling."""

    if argv is None:
        argv = sys.argv

    # Defaults
    show_tags = False
    show_descriptions = False
    show_notes = False

    search_options = [
        'tag',
        'ntag',
        'desc',
        'ndesc',
        'note',
        'nnote',
        'url',
        'nurl',
        'etag',
        'edesc',
        'enote',
        'eurl']

    # Initialize search function parameters
    search_params = {}
    for search_option in search_options:
        search_params[search_option] = []

    try:
        try:
            opts, args = getopt.getopt(
                argv[1:],
                'tdn',
                [search_option + '=' for search_option in search_options])
        except getopt.GetoptError, err:
            raise Usage(err.msg)

        if len(opts) != 0:
            for option, value in opts:
                if option in [
                    '--' + search_option for search_option in search_options]:
                    search_params[option[2:]].append(value)
                elif option == '-t':
                    show_tags = True
                elif option == '-d':
                    show_descriptions = True
                elif option == '-n':
                    show_notes = True
                else:
                    raise Usage('Unhandled option %s' % option)

    except Usage, err:
        sys.stderr.write(err.msg + '\n')
        return 2

    bookmarks = DeliciousBookmarks(ET.fromstring(sys.stdin.read()))
    bookmarks.search(search_params)

    print(bookmarks.pretty_print(show_tags, show_descriptions, show_notes))


if __name__ == '__main__':
    sys.exit(main())
