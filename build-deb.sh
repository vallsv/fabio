#!/bin/sh
rm -rf dist
python setup.py sdist
cd dist
tar -xzf  fabio-*.tar.gz
cd fabio*
export DEB_BUILD_OPTIONS=nocheck
python setup.py --command-packages=stdeb.command bdist_deb
sudo dpkg -i deb_dist/python-fabio*.deb
cd ../..

