Name:		bdii
Version:	5.2.4
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

%if %{?fedora}%{!?fedora:0} >= 5 || %{?rhel}%{!?rhel:0} >= 5
Requires(post):         policycoreutils
Requires(postun):       policycoreutils
%if %{?fedora}%{!?fedora:0} >= 11 || %{?rhel}%{!?rhel:0} >= 6
Requires(post):         policycoreutils-python
Requires(postun):       policycoreutils-python
%endif
%endif

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

 
%post
sed "s/\(rootpw *\)secret/\1$(mkpasswd -s 0 | tr '/' 'x')/" \
    -i %{_sysconfdir}/%{name}/bdii-slapd.conf
/sbin/chkconfig --add %{name}
%if %{?fedora}%{!?fedora:0} >= 5 || %{?rhel}%{!?rhel:0} >= 5
semanage port -a -t ldap_port_t -p tcp 2170 2>/dev/null || :
semanage fcontext -a -t slapd_db_t "%{_localstatedir}/run/%{name}(/.*)?" 2>/dev/null || :
%endif

%preun
if [ $1 = 0 ]; then
  service %{name} stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ]; then
  service %{name} condrestart > /dev/null 2>&1
fi
%if %{?fedora}%{!?fedora:0} >= 5 || %{?rhel}%{!?rhel:0} >= 5
if [ $1 -eq 0 ]; then
  semanage port -d -t ldap_port_t -p tcp 2170 2>/dev/null || :
  semanage fcontext -d -t slapd_db_t "%{_localstatedir}/run/%{name}(/.*)?" 2>/dev/null || :
fi
%endif

%files
%defattr(-,root,root,-)
%attr(-,ldap,ldap) %{_localstatedir}/lib/%{name}
%attr(-,ldap,ldap) %{_localstatedir}/log/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/DB_CONFIG
%config(noreplace) /etc/%{name}/bdii.conf
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
%doc /usr/share/man/man1/

%changelog
* Fri Jul 8 2011 Laurence Field <laurence.field@cern.ch> - 5.2.4-1
- Fix for IS-245
* Mon Apr 18 2011 Laurence Field <laurence.field@cern.ch> - 5.2.3-1
- Fix for IS-232
* Mon Apr 18 2011 Laurence Field <laurence.field@cern.ch> - 5.2.2-1
- Added SE Linux profile to address IS-231
* Tue Apr 05 2011 Laurence Field <laurence.field@cern.ch> - 5.2.1-1
- Addressed cron job error due to FHS change
* Tue Mar 08 2011 Laurence Field <laurence.field@cern.ch> - 5.2.0-1
- Addressed IS-2225, Now FHS compliant
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
