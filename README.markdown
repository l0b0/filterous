filterous - Search/filter your Delicious bookmark backups
=========

Installation
------------

    make
    sudo make install

Documentation
-------------

    filterous --help

Examples
--------

Unread stuff:

    filterous -dtnb --tag toread --ntag read < bookmarks.xml

Find duplicated bookmark descriptions (possible content duplicates):

    filterous -Td < bookmarks.xml | awk -F $'\t' 'x[$2]++ == 1 { print $2 }'
