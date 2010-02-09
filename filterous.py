#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Filterous - Delicious Command Line Filter

Default syntax:

./filterous.py < all.xml

Options:
--tag       Tag search string (@tag)
--ntag      Negated tag search string (@tag)
--desc      Description search string (@description)
--ndesc     Negated description search string (@description)
--notes     Notes search string (@extended)
--nnotes    Negated notes search string (@extended)
--url       URL search string (@href)
--nurl      Negated URL search string (@href)

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

./filterous.py --nurl='^https' < all.xml
    Returns non-HTTPS links.

./filterous.py --ntag='^for:' --tag='★★★★★' < all.xml
    Returns great links that you have not shared with your contacts.
"""

__author__ = 'Victor Engmark'
__email__ = 'victor.engmark@gmail.com'
__url__ = 'http://filterous.sourceforge.net/'
__copyright__ = 'Copyright (C) 2010 Victor Engmark'
__license__ = 'GPLv3'

from datetime import datetime
import xml.etree.ElementTree as ET
import re

class Bookmarks():
    """Has a list of bookmarks with their metadata and display functions."""
    def __init__(self, text):
        self.doc = ET.fromstring(text)

    def __str__(self):
        return ET.tostring(self.doc)

    def search(self, tags):
        """
        Find matching bookmarks.

        @param tags: List of tag regexes to match
        @return: List of URLs
        """

        tag_patterns = [re.compile(tag) for tag in tags]

        for node in self.doc.getchildren():
            for tag_pattern in tag_patterns:
                match = False
                for node_tag in node.attrib['tag'].split(' '):
                    if tag_pattern.match(node_tag):
                        match = True
                if not match:
                    self.doc.remove(node)

        # Update @update
        #xml_root.setProp('update', datetime.utcnow().isoformat()[:-7] + 'Z')
