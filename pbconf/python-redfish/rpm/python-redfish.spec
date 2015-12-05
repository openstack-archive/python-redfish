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

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__mkdir} -p %{buildroot}/%{_bindir}
install -m 755 redfish-client/redfish-client.py %{buildroot}/%{_bindir}/redfish-client
rm -fr %{buildroot}/%{python_sitelib}/redfish/old

%files
%doc README.rst examples/[a-z]*.py LICENSE
%dir %{python_sitelib}/redfish
%{_bindir}/redfish-client
%{python_sitelib}/redfish/*.py*
%{python_sitelib}/redfish/tests/*.py*
%{python_sitelib}/python_redfish*

%changelog
PBLOG

