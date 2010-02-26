#!/bin/sh

python setup.py test && python setup.py $1 sdist bdist_rpm bdist_wininst upload clean
