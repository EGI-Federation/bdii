Name:		bdii
Version:	5.1.23
Release:	1%{?dist}
Summary:	The Berkeley Database Information Index (BDII)

Group:		System Environment/Daemons
License:	ASL 2.0
URL:		https://twiki.cern.ch/twiki/bin/view/EGEE/BDII
#               wget -O %{name}-%{version}-443.tar.gz "http://svnweb.cern.ch/world/wsvn/gridinfo/bdii/tags/R_5_1_0?op=dl&rev=443"
Source:		%{name}-%{version}.tar.gz
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
Requires(preun):        lsb
Requires(postun):	initscripts
Requires(postun):       lsb

%description
The Berkeley Database Information Index (BDII)

%prep
%setup -q
#change to the one below if you are building against downloaded tarball from svnweb.cern.ch
#%setup -q -n trunk.r443

%build
# Nothing to build

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}

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

%pre
# Stop service if upgrading from version 5.0 to 5.1
if [ -f /opt/bdii/bin/bdii-update ]; then 
	service %{name} stop > /dev/null 2>&1
	if [ -f /var/log/bdii/bdii-update.log ]; then
	    rm -f /var/log/bdii/bdii-update.log
	fi
fi
 
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
%attr(-,ldap,ldap) %{_localstatedir}/lib/%{name}
%attr(-,ldap,ldap) /opt/glite/etc/gip
%attr(-,ldap,ldap) %{_localstatedir}/log/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/DB_CONFIG
%config(noreplace) /opt/%{name}/etc/bdii.conf
%config(noreplace) /etc/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/BDII.schema
%config(noreplace) %attr(-,ldap,ldap) %{_sysconfdir}/%{name}/bdii-slapd.conf
%config(noreplace) %attr(-,ldap,ldap) %{_sysconfdir}/%{name}/bdii-top-slapd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/cron.d/bdii-proxy
%{_initrddir}/%{name}
%{_sbindir}/bdii-update
%{_sbindir}/bdii-proxy
%doc copyright

%changelog
* Wed Mar 02 2011 Laurence Field <laurence.field@cern.ch> - 5.1.23-1
- Addressed IS-219
* Wed Feb 23 2011 Laurence Field <laurence.field@cern.ch> - 5.1.22-1
- Addressed IS-218
* Tue Feb 15 2011 Laurence Field <laurence.field@cern.ch> - 5.1.21-1
- Increase RAM disk size to 1500M
* Wed Feb 9 2011 Laurence Field <laurence.field@cern.ch> - 5.1.19-1
- Address IS-209, IS-211
* Wed Feb 2 2011 Laurence Field <laurence.field@cern.ch> - 5.1.17-1
- Address IS-192, IS-194, IS-195, IS-196, IS-197, IS-198, IS-200
* Mon Jan 31 2011 Laurence Field <laurence.field@cern.ch> - 5.1.16-1
- Added IS-179, delayed delete function
* Fri Nov 26 2010 Laurence Field <laurence.field@cern.ch> - 5.1.11-1
- Fixed IS-96, IS-160, IS-163, IS-164, IS-165, IS-172
* Mon Sep 06 2010 Laurence Field <laurence.field@cern.ch> - 5.1.9-1
- Fixed IS-145
* Thu May 20 2010 Laurence Field <laurence.field@cern.ch> - 5.1.5-1
- Added /opt/glite/etc/gip
* Mon Mar 29 2010 Laurence Field <laurence.field@cern.ch> - 5.1.0-1
- New stable version
* Thu Feb 25 2010 Daniel Johansson <daniel@nsc.liu.se> - 5.0.8-2.443
- Update packaging etc (svn revision 443)
* Wed Feb 24 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0.8-2.436
- Update (svn revision 436)
* Mon Feb 08 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0.8-1
- Initial package (svn revision 375)
