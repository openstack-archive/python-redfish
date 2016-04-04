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
# Fix for now as long as setuptools isn't more recent in distributions
PBPYTHON3FILTER
%{__python} setup.py build

# Build minimal documentation
cd doc
make man
make singlehtml
make latexpdf

%install
./install.sh %{buildroot} %{python_sitelib} %{_prefix} #%{_logdir}

%files
%doc README.rst examples/[a-z]*.py LICENSE
%doc doc/build/latex/*.pdf
%{_bindir}/redfish-client
%dir %{_datadir}/redfish-client
%{_datadir}/redfish-client/templates/*
%config(noreplace) %{_sysconfdir}/redfish-client.conf
%dir %{python_sitelib}/redfish
%{python_sitelib}/redfish/*.py*
%{python_sitelib}/redfish/tests/*.py*
%{python_sitelib}/python_redfish*
%{_mandir}/man1/*
%{_docdir}/PBREALPKG/html/_static/*
%{_docdir}/PBREALPKG/html/index.html
#%{_logdir}/PBREALPKG
%changelog
PBLOG
