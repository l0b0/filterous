#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Filterous - Delicious Command Line Filter <http://filterous.sourceforge.net/>

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
-T         Output tab separated list for easier parsing
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

./filterous.py -t --tag=video --tag=tosee --ntag=seen < all.xml
    Show links to unseen videos with their tags.

./filterous.py --nurl=https:// < all.xml
    Show non-HTTPS links.

./filterous.py -dntT --ntag=for: --tag=★★★★★ < all.xml
    Returns great links that you have not shared with your contacts as a tab-
    separated list with URL, description, notes and tags.
"""

__author__ = 'Victor Engmark'
__email__ = 'victor.engmark@gmail.com'
__copyright__ = 'Copyright (C) 2010 Victor Engmark'
__license__ = 'GPLv3'

import getopt
from lxml import etree
import sys

# pylint: disable-msg=W0105
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

ATTRIBUTES_READABLE = {
    'tag': 'Tags',
    'description': 'Title',
    'extended': 'Notes',
    'href': 'URL'}

ATTRIBUTES_REQUIRED = ['description', 'href']

ERRM_SUBMIT_BUG = u'Please submit a bug report at \
<https://sourceforge.net/tracker/?func=add&group_id=303845&atid=1280761>, \
including the output of this script.'
"""Ask users for feedback."""

def _get_format_xpath(attributes, human_readable):
    """
    Pretty printing XPath for each post element.

    @param attributes: List of attributes to print
    @return: XPath
    """
    assert(attributes is not None)
    assert(len(attributes) != 0)

    # Newline separated for readability or tab separated for parsing
    if human_readable:
        attribute_separator = '\n'
        post_separator = '\n\n'
    else:
        attribute_separator = '\t'
        post_separator = '\n'

    show_prefix = human_readable and len(attributes) != 1

    result = 'concat('

    for attribute in attributes:
        assert(attribute in PARAM_ATTRIBUTES.values())

        if show_prefix:
            result += '"%s: ", ' % ATTRIBUTES_READABLE[attribute]

        result += '@%s, ' % attribute

        if attribute != attributes[-1]:
            result += '"%s", ' % attribute_separator
        else:
            result += '"%s"' % post_separator

    result += ')'

    return etree.XPath(result)


def _get_search_xpath(terms):
    """
    XPath expression to search on each post.

    @param terms: Dictionary of terms, each with a list of values to search for
    @return: XPath
    """
    result = ''

    for term, values in terms.items():
        if term not in PARAM_ATTRIBUTES:
            raise NameError('Not a valid search term: %s' % term)

        attribute = PARAM_ATTRIBUTES[term]

        xpaths = []
        for index in range(len(values)):
            value = values[index]
            if isinstance(value, str):
                values[index] = value.decode("utf-8")

        if term in SS_STRING_MATCHES:
            for value in values:
                # Simpler to add spaces at the ends than to split and search
                xpaths.append(
                    u"contains(\
concat(' ', @%(x_attribute)s, ' '), \
concat(' ', '%(x_value)s', ' '))" % {
                        'x_attribute': attribute,
                        'x_value': value})
        elif term in SUBSTRING_MATCHES:
            for value in values:
                xpaths.append(
                    u"contains(@%(x_attribute)s, '%(x_value)s')" % {
                        'x_attribute': attribute,
                        'x_value': value})
        else:
            raise NameError('Method unknown for search term: %s' % term)

        if xpaths != []:
            if term in NEGATIVE_MATCHES:
                xpaths = [u'not(%s)' % xpath for xpath in xpaths]
            elif term not in POSITIVE_MATCHES:
                raise NameError('Unsupported search term: %s' % term)

            xpaths = [u'[%s]' % xpath for xpath in xpaths]

        result += u''.join(xpaths)

    return etree.XPath('/posts/post' + result)


def search(file_pointer, out, terms, show_attributes, human_readable = True):
    """
    Get only the posts that match the terms.

    @param file_pointer: Delicious bookmark export file pointer
    @param terms: Dictionary of search terms
    @param show_attributes: Which attributes to output
    @param out: Output stream
    """
    search_xpath = _get_search_xpath(terms)
    format_xpath = _get_format_xpath(show_attributes, human_readable)

    context = etree.iterparse(file_pointer, tag='posts')

    for event_elem in context:
        matches = search_xpath(event_elem[1])
        if matches is None:
            print('No matches found.')
            return

        for match in matches:
            out.write(''.join(format_xpath(match).encode('utf8')))


class UsageError(ValueError):
    """Raise in case of invalid parameters."""
    # pylint: disable-msg=W0231
    def __init__(self, msg):
        self.msg = msg


def main(argv = None):
    """Argument handling."""

    if argv is None:
        argv = sys.argv

    # Defaults
    show_attributes = ['href']
    human_readable = True

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
                'dntT',
                search_opts)[0]
        except getopt.GetoptError, err:
            raise UsageError(err.msg)

        if opts == []:
            raise UsageError(__doc__)

        for option, value in opts:
            if option in search_options:
                search_params[option[2:]].append(value)
            elif option == '-d':
                show_attributes.append('description')
            elif option == '-n':
                show_attributes.append('extended')
            elif option == '-t':
                show_attributes.append('tag')
            elif option == '-T':
                human_readable = False
            else:
                raise UsageError(
                    "Unhandled option '%(x_option)s'. %(x_user_action)s" % {
                        'x_option': option,
                        'x_user_action': ERRM_SUBMIT_BUG})

    except UsageError, err:
        sys.stderr.write(err.msg + '\n')
        return 2

    search(
        sys.stdin,
        sys.stdout,
        search_params,
        show_attributes,
        human_readable)

if __name__ == '__main__':
    sys.exit(main())
