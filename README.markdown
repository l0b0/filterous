filterous - Search/filter your Delicious bookmark backups
=========

Installation
------------

    make
    sudo make install

Search tips
-----------

Duplicated bookmark descriptions (possible content duplicates):

    filterous -Td < bookmarks.xml | awk -F $'\t' 'x[$2]++ == 1 { print $2 }'
