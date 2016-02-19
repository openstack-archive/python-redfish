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
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# This will go in a separate script later on to share with other distros
rm -fr %{buildroot}/%{python_sitelib}/redfish/old

for i in 1; do
	mkdir -p %{buildroot}/%{_mandir}/man$i
	install -m 644 doc/build/man/*.$i %{buildroot}/%{_mandir}/man$i
done
install -d 755 %{buildroot}/%{_docdir}/%{name}/html/_static
install -m 644 doc/build/singlehtml/*.html %{buildroot}/%{_docdir}/%{name}/html
install -m 644 doc/build/singlehtml/_static/* %{buildroot}/%{_docdir}/%{name}/html/_static

%files
%doc README.rst examples/[a-z]*.py LICENSE
%doc doc/build/latex/*.pdf
%dir %{python_sitelib}/redfish
%dir %{_docdir}/%{name}/html
%{_docdir}/%{name}/html/*.html
%dir %{_docdir}/%{name}/html/_static
%{_docdir}/%{name}/html/_static/*
%{_bindir}/redfish-client
%{python_sitelib}/redfish/*.py*
%{python_sitelib}/redfish/tests/*.py*
%{python_sitelib}/python_redfish*
%{_mandir}/man1/*
%changelog
PBLOG
