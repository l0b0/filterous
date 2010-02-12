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

try:
    from lxml import etree
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree
                except ImportError:
                    sys.stdout.write('Failed to import ElementTree from any known place\n')

TAG_SEPARATOR = u' '
"""Delicious separates tags with spaces"""

POSITIVE_MATCHES = set(['tag', 'desc', 'note', 'url'])
"""Values which /must/ be in the posts"""

NEGATIVE_MATCHES = set(['ntag', 'ndesc', 'nnote', 'nurl'])
"""Values which must /not/ be in the posts"""

SS_STRING_MATCHES = set(['tag', 'ntag'])
"""Match full string in a space separated list"""

SUBSTRING_MATCHES = set(['desc', 'ndesc', 'note', 'nnote', 'url', 'nurl'])
"""Match any substring"""

PARAM_ATTRIBUTES = {
    'tag': 'tag',
    'ntag': 'tag',
    'desc': 'description',
    'ndesc': 'description',
    'note': 'extended',
    'nnote': 'extended',
    'url': 'href',
    'nurl': 'href'}
"""Map command line options to XML attribute names"""

def get_format_xpath(attributes):
    """
    Pretty printing XPath.

    @param attributes: List of attributes to print
    @return: XPath
    """

    attribute_paths = []

    for attribute in attributes:
        if attribute not in PARAM_ATTRIBUTES.values():
            raise NameError('Unknown attribute: %s' % attribute)
        attribute_paths.append('@' + attribute)

    if len(attributes) == 1:
        result = 'concat(string(' + attribute_paths[0] + "), '\n')"
    else:
        result = 'concat(' + \
                 ", '\n', ".join(attribute_paths) + \
                 ", '\n\n')"

    return etree.XPath(result)


def get_search_xpath(terms):
    """
    XPath expression to search on each post.

    @param terms: Dictionary of terms, each with values to be searched for
    @param attributes: List of attributes to print
    @return: XPath
    """
    result = ''

    for term, values in terms.items():
        if term not in PARAM_ATTRIBUTES:
            raise NameError('Not a valid search term: %s' % term)

        attribute = PARAM_ATTRIBUTES[term]

        xpaths = []
        if term in SS_STRING_MATCHES:
            for value in values:
                xpaths.append(
                    "contains(\
concat(' ', @%(x_attribute)s, ' '), \
concat(' ', '%(x_value)s', ' '))" % {
                        'x_attribute': attribute,
                        'x_value': value})
        elif term in SUBSTRING_MATCHES:
            for value in values:
                xpaths.append(
                    "contains(@%(x_attribute)s, '%(x_value)s')" % {
                        'x_attribute': attribute,
                        'x_value': value})
        else:
            raise NameError('Method unknown for search term: %s' % term)

        if xpaths != []:
            if term in NEGATIVE_MATCHES:
                xpaths = ['not(%s)' % xpath for xpath in xpaths]
            elif term not in POSITIVE_MATCHES:
                raise NameError('Unsupported search term: %s' % term)

            xpaths = ['[%s]' % xpath for xpath in xpaths]

        result += ''.join(xpaths)

    return '/posts/post' + result


def write_if_node(out, node):
    if node is not None:
        out.write(etree.tostring(node, encoding='utf-8'))


def search(file_pointer, terms, show_attributes, out):
    """
    Get only the posts that match the terms.

    @param file_pointer: Delicious bookmark export file pointer
    @param terms: Dictionary of search terms
    @param show_attributes: Which attributes to output
    @param out: Output stream
    """
    search_xpath = get_search_xpath(terms)
    format_xpath = get_format_xpath(show_attributes)

    context = etree.iterparse(file_pointer, tag='posts')

    for event, elem in context:
        matches = elem.xpath(search_xpath)
        if matches is None:
            print('No matches found.')
            return

        for match in matches:
            out.write(''.join(format_xpath(match).encode('utf8')))

class Usage(Exception):
    """Raise in case of invalid parameters."""
    # pylint: disable-msg=W0231
    def __init__(self, msg):
        self.msg = msg


def main(argv = None):
    """Argument handling."""

    if argv is None:
        argv = sys.argv

    # Default attributes in output
    show_attributes = ['href']

    search_option_names = PARAM_ATTRIBUTES.keys()
    search_opts = [option + '=' for option in search_option_names]
    search_options = ['--' + option for option in search_option_names]

    # Initialize search function parameters
    search_params = {}
    for search_option in search_option_names:
        search_params[search_option] = []

    try:
        try:
            opts = getopt.getopt(
                argv[1:],
                'tdn',
                search_opts)[0]
        except getopt.GetoptError, err:
            raise Usage(err.msg)

        if opts == []:
            raise Usage(__doc__)

        for option, value in opts:
            if option in search_options:
                search_params[option[2:]].append(value)
            elif option == '-t':
                show_attributes.append('tag')
            elif option == '-d':
                show_attributes.append('description')
            elif option == '-n':
                show_attributes.append('extended')
            else:
                raise Usage('Unhandled option %s' % option)

    except Usage, err:
        sys.stderr.write(err.msg + '\n')
        return 2

    search(sys.stdin, search_params, show_attributes, sys.stdout)

if __name__ == '__main__':
    sys.exit(main())
