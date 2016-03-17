#!/bin/bash

# Syntax: install.sh <Root Dir> <Python SiteLib> <Prefix>
set -x 

export rootdir=$1
export sitelib=$2
export prefix=$3
#python setup.py install --skip-build --prefix=$prefix
python setup.py install --skip-build --root=$rootdir --prefix=$prefix
rm -rf $rootdir/$sitelib/redfish/old

for i in 1; do
	mkdir -p $rootdir/$prefix/share/man/man$i
	install -m 644 doc/build/man/*.$i $rootdir/$prefix/share/man/man$i
done
install -d 755 $rootdir/$prefix/share/doc/PBPKG/html/_static
install -m 644 doc/build/singlehtml/*.html $rootdir/$prefix/share/doc/PBPKG/html
install -m 644 doc/build/singlehtml/_static/* $rootdir/$prefix/share/doc/PBPKG/html/_static
# Hardcoded for now to solve the delivery of the conf file still not correct with setup.py
mkdir -p $rootdir/etc
mv $rootdir/$prefix/etc/redfish-client.conf $rootdir/etc/redfish-client.conf
