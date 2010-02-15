Name:		bdii
Version:	5.0.8
Release:	1%{?dist}
Summary:	The Berkeley Database Information Index (BDII)

Group:		System Environment/Daemons
License:	ASL 2.0
URL:		https://twiki.cern.ch/twiki/bin/view/EGEE/BDII
Source:		%{name}-%{version}.tar.gz
#Patch0:		%{name}.patch
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires:	openldap-clients
Requires:	openldap-servers
Requires:	lsb
Requires:	glue-schema >= 2.0.0

Requires(post):		chkconfig
Requires(post):		expect
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%description
The Berkeley Database Information Index (BDII)

%prep
%setup -q -c
#%patch0 -p1

%build
# Nothing to build

%install
rm -rf %{buildroot}
make -f INSTALL install prefix=%{buildroot}

# Turn off default enabling of the service
if [ -f %{buildroot}%{_initrddir}/%{name} ]; then
    sed -e 's/\(chkconfig: \)\w*/\1-/' \
        -e '/Default-Start/d' \
        -e 's/\(Default-Stop:\s*\).*/\10 1 2 3 4 5 6/' \
        -i %{buildroot}%{_sysconfdir}/init.d/%{name}
else
    mkdir -p %{buildroot}%{_initrddir}
    sed -e 's/\(chkconfig: \)\w*/\1-/' \
	-e '/Default-Start/d' \
	-e 's/\(Default-Stop:\s*\).*/\10 1 2 3 4 5 6/' \
	%{buildroot}%{_sysconfdir}/init.d/%{name} > %{buildroot}%{_initrddir}/%{name}
    rm %{buildroot}%{_sysconfdir}/init.d/%{name}
fi
chmod 0755 %{buildroot}%{_initrddir}/%{name}


%clean
rm -rf %{buildroot}

%post
sed "s/\(rootpw *\)secret/\1$(mkpasswd -s 0 | tr '/' 'x')/" \
    -i %{_sysconfdir}/%{name}/bdii-slapd.conf
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
  service %{name} stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ]; then
  service %{name} condrestart > /dev/null 2>&1
fi

%files
%defattr(-,root,root,-)
%attr(-,ldap,ldap) %{_localstatedir}/%{name}
%attr(-,ldap,ldap) %{_localstatedir}/lib/%{name}
%attr(-,ldap,ldap) %{_localstatedir}/log/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/DB_CONFIG
%config(noreplace) %{_sysconfdir}/%{name}/bdii.conf
%config(noreplace) %{_sysconfdir}/%{name}/BDII.schema
%config(noreplace) %{_sysconfdir}/%{name}/bdii-slapd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/cron.d/bdii-proxy
%{_initrddir}/%{name}
%{_sbindir}/bdii-update
%{_sbindir}/bdii-proxy

%changelog
* Mon Feb 08 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0.8-1
- Initial package
