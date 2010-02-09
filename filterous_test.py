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

import filterous

class TestTag(unittest.TestCase):
    """Test tag search option"""
    def test_empty_tag(self):
        """Empty tag"""
        try:
            filterous.DeliciousSearch(
                filename = 'all.xml',
                [''],
                True)
            self.fail('Invalid vCard created')
        except vcard.VCardFormatError as error:
            self.assertEquals(error.message, vcard.MSG_EMPTY_VCARD)

def main():
    """Command line options checkpoint"""
    unittest.main()

if __name__ == '__main__':
    main()
