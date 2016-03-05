#!/bin/bash

# Syntax: install.sh <Root Dir> <Python SiteLib> <Prefix>

export rootdir=$1
export sitelib=$2
export prefix=$3
python setup.py install --skip-build --root $rootdir
rm -rf $rootdir/$sitelib/redfish/old

for i in 1; do
	mkdir -p $rootdir/$prefix/man/man$i
	install -m 644 doc/build/man/*.$i $rootdir/$prefix/man/man$i
done
install -d 755 $rootdir/$prefix/doc/PBPKG/html/_static
install -m 644 doc/build/singlehtml/*.html $rootdir/$prefix/doc/PBPKG/html
install -m 644 doc/build/singlehtml/_static/* $rootdir/$prefix/doc/PBPKG/html/_static
