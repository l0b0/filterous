#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Filterous - Delicious bookmark backup search

Default syntax:

./filterous.py -f username.xml [[--not] [--tag='string'] [--description='string']
[--notes='string'] [--url='string'] ...]

Options:
-f,--file                   Path to Delicious export file
<https://api.del.icio.us/v1/posts/all?>
--not                       Negate the next search operator
-t,--tag                    Tag search string (@tag)
-d,--description            Description search string (@description)
-e,-n,--extended,--notes    Notes search string (@extended)
-h,-u,--href,--url          URL search string (@href)
-v,--verbose                Verbose output

Description:
Will search the tags of the XML file downloaded from
<https://api.del.icio.us/v1/posts/all?>. To avoid the slow load of that page in
a web browser, you can use the following command:
curl -ku : https://api.del.icio.us/v1/posts/all

Examples:

./filterous.py -f username.xml --tag='video' --tag='tosee' --not --tag='seen'
Returns links to unseen videos

./filterous.py -f username.xml --not --href='^https'
Returns non-secured links

./filterous.py -f username.xml --not --tag='^for:' --tag='★★★★★'
Returns great links that you have not shared with your contacts

./filterous.py -f username.xml --verbose
Returns a list of all your bookmarks, with all the user provided information
included
"""

__author__ = 'Victor Engmark'
__email__ = 'victor.engmark@gmail.com'
__url__ = 'http://filterous.sourceforge.net/'
__copyright__ = 'Copyright (C) 2010 Victor Engmark'
__license__ = 'GPLv3'

import getopt
import sys
import libxml2

class DeliciousSearch():
    """
    Has a list of bookmarks with their metadata and display functions
    """
    def __init__(self, filename, tags = [], verbose = False):
        self.filename = filename
        self.verbose = verbose
        self.tags = tags

        self.result = self.search()

    def __str__(self):
        return '\n'.join(self.result)

    def search(self):
        """
        Find matching bookmarks
        @param filename: Delicious bookmark file path
        @param tags: Tags to match
        @return: List of URLs
        """
        doc = libxml2.parseFile(self.filename)
        result = []

        tag_searches = ["contains(@tag,'%s')" % tag for tag in self.tags]
        tag_search = ' and '.join(tag_searches)
        if len(tag_search) != 0:
            tag_search = '[' + tag_search + ']'

        try:
            for bookmark_element in doc.xpathEval('/posts/post' + tag_search):
                result.append(bookmark_element.xpathEval('@href')[0].content)
        except SyntaxError, error:
            sys.stderr.write(
                'Could not process search %s: %s' % (
                    tag_search,
                    error))
        finally:
            doc.freeDoc()

        return result

class Usage(Exception):
    """Raise in case of invalid parameters"""
    def __init__(self, msg):
        self.msg = msg

def main(argv = None):
    """Argument handling"""

    if argv is None:
        argv = sys.argv

    # Defaults
    verbose = False
    filename = ''
    tags = []

    try:
        try:
            opts, args = getopt.getopt(
                argv[1:],
                'vf:t:',
                [
                    'verbose',
                    'file=',
                    'tag='])
        except getopt.GetoptError, err:
            raise Usage(err.msg)

        for option, value in opts:
            if option in ('-v', '--verbose'):
                verbose = True
            elif option in ('-f', '--file'):
                filename = value
            elif option in ('-t', '--tag'):
                tags.append(value)
            else:
                raise Usage('Unhandled option %s' % option)

        if args or not filename:
            raise Usage(__doc__)

        result = DeliciousSearch(filename, tags, verbose)

        print(result)

    except Usage, err:
        sys.stderr.write(err.msg + '\n')
        return 2

if __name__ == '__main__':
    sys.exit(main())
