#
# $Id$
#

Name:           PBREALPKG
Version:        PBVER
Release:        PBTAGPBSUF
Summary:        PBSUMMARY

License:        PBLIC
Group:          PBGRP
Url:            PBURL
Source:         PBREPO/PBSRC
Requires:       PBDEP
BuildArch:      noarch
BuildRequires:  PBBDEP

%description
PBDESC

%prep
%setup -q

%build
%{__python} setup.py build
# Deal with doc
cd doc
make man
make singlehtml
make latexpdf

%install
./install.sh %{buildroot} %{python_sitelib} %{_prefix}

%files
%doc README.rst examples/[a-z]*.py LICENSE
%doc doc/build/latex/*.pdf
%doc %{_docdir}/%{name}/html
%doc %{_docdir}/%{name}/html/*.html
%doc %{_docdir}/%{name}/html/_static
%doc %{_docdir}/%{name}/html/_static/*
%{_bindir}/redfish-client
# add conf file
# add template
%dir %{python_sitelib}/redfish
%{python_sitelib}/redfish/*.py*
%{python_sitelib}/redfish/tests/*.py*
%{python_sitelib}/python_redfish*
%{_mandir}/man1/*
%changelog
PBLOG
