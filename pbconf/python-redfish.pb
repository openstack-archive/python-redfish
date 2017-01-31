#
# Project Builder configuration file
# For project python-redfish
#
# $Id$
#

#
# What is the project URL
#
#pburl python-redfish = svn://svn.python-redfish.org/python-redfish/devel
#pburl python-redfish = svn://svn+ssh.python-redfish.org/python-redfish/devel
#pburl python-redfish = cvs://cvs.python-redfish.org/python-redfish/devel
#pburl python-redfish = http://www.python-redfish.org/src/python-redfish-devel.tar.gz
#pburl python-redfish = ftp://ftp.python-redfish.org/src/python-redfish-devel.tar.gz
#pburl python-redfish = file:///src/python-redfish-devel.tar.gz
#pburl python-redfish = dir:///src/python-redfish-devel
pburl python-redfish = git+https://review.openstack.org/p/openstack/python-redfish.git

# Repository
pbrepo python-redfish = ftp://ftp.mondorescue.org
pbml python-redfish = python-redfish@mondorescue.org
pbsmtp python-redfish = localhost
# For distro supporting it, which area is used
#projcomponent python-redfish = main

# Check whether project is well formed 
# when downloading from ftp/http/...
# (containing already a directory with the project-version name)
pbwf python-redfish = 1

# Do we check GPG keys
pbgpgcheck python-redfish = 1

#
# Packager label
#
pbpackager python-redfish = Bruno Cornec <bruno@project-builder.org>
#

# For delivery to a machine by SSH (potentially the FTP server)
# Needs hostname, account and directory
#
sshhost python-redfish = www.mondorescue.org
sshlogin python-redfish = bruno
sshdir python-redfish = /prj/ftp
sshport python-redfish = 22
#

#
# For Virtual machines management
# Naming convention to follow: distribution name (as per ProjectBuilder::Distribution)
# followed by '-' and by release number
# followed by '-' and by architecture
# a .vmtype extension will be added to the resulting string
# a QEMU rhel-3-i286 here means that the VM will be named rhel-3-i386.qemu
#
vmlist python-redfish = opensuse-12.3-i386,debian-8-i386,ubuntu-16.04-i386,mageia-5-i386,mageia-5-x86_64,fedora-23-x86_64,rhel-7-x86_64,opensuse-12.3-x86_64,sles-12-x86_64,debian-8-x86_64,ubuntu-16.04-x86_64

#
# Valid values for vmtype are
# qemu, (vmware, xen, ... TBD)
#vmtype python-redfish = qemu

# Hash for VM stuff on vmtype
#vmntp default = pool.ntp.org

# We suppose we can commmunicate with the VM through SSH
#vmhost python-redfish = localhost
#vmlogin python-redfish = pb
#vmport python-redfish = 2222

# Timeout to wait when VM is launched/stopped
#vmtmout default = 120

# per VMs needed paramaters
#vmopt python-redfish = -m 384 -daemonize
#vmpath python-redfish = /home/qemu
#vmsize python-redfish = 5G

# 
# For Virtual environment management
# Naming convention to follow: distribution name (as per ProjectBuilder::Distribution)
# followed by '-' and by release number
# followed by '-' and by architecture
# a .vetype extension will be added to the resulting string
# a chroot rhel-3-i286 here means that the VE will be named rhel-3-i386.chroot
#
#velist python-redfish = fedora-7-i386

# VE params
vetype python-redfish = docker
#ventp default = pool.ntp.org
#velogin python-redfish = pb
#vepath python-redfish = /var/cache/rpmbootstrap
#rbsconf python-redfish = /etc/mock
#verebuild python-redfish = false

#
# Global version/tag for the project
#
projver python-redfish = 0.4
projtag python-redfish = 1

# Hash of valid version names

# Additional repository to add at build time
# addrepo centos-5-x86_64 = http://packages.sw.be/rpmforge-release/rpmforge-release-0.3.6-1.el5.rf.x86_64.rpm,ftp://ftp.project-builder.org/centos/5/pb.repo
# addrepo centos-5-x86_64 = http://packages.sw.be/rpmforge-release/rpmforge-release-0.3.6-1.el5.rf.x86_64.rpm,ftp://ftp.project-builder.org/centos/5/pb.repo
#version python-redfish = devel,stable

# Is it a test version or a production version
testver python-redfish = true
# Which upper target dir for delivery
delivery python-redfish = test

# Additional repository to add at build time
# addrepo centos-5-x86_64 = http://packages.sw.be/rpmforge-release/rpmforge-release-0.3.6-1.el5.rf.x86_64.rpm,ftp://ftp.project-builder.org/centos/5/pb.repo
# addrepo centos-4-x86_64 = http://packages.sw.be/rpmforge-release/rpmforge-release-0.3.6-1.el4.rf.x86_64.rpm,ftp://ftp.project-builder.org/centos/4/pb.repo

# Adapt to your needs:
# Optional if you need to overwrite the global values above
#
#pkgver python-redfish = stable
#pkgtag python-redfish = 3
# Hash of default package/package directory
defpkgdir python-redfish = .
# Hash of additional package/package directory
#extpkgdir minor-pkg = dir-minor-pkg

# List of files per pkg on which to apply filters
# Files are mentioned relatively to pbroot/defpkgdir
filteredfiles python-redfish = redfish-client/redfish-client,doc/source/conf.py,redfish-client/etc/redfish-client.conf,install.sh
#supfiles python-redfish = python-redfish.init

# We use pbr to generate sources
pbpbr python-redfish = 1
