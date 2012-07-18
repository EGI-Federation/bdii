Name:		bdii
Version:	5.2.11
Release:	1%{?dist}
Summary:	The Berkeley Database Information Index (BDII)

Group:		System Environment/Daemons
License:	ASL 2.0
URL:		https://twiki.cern.ch/twiki/bin/view/EGEE/BDII
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export http://svnweb.cern.ch/guest/gridinfo/bdii/tags/R_5_2_11 %{name}-%{version}
#  tar --gzip -czvf %{name}-%{version}.tar.gz %{name}-%{version} 

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires:	openldap-clients
Requires:	openldap-servers
Requires:	glue-schema >= 2.0.0

Requires(post):		chkconfig
Requires(post):		expect
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts

%if %{?fedora}%{!?fedora:0} >= 5 || %{?rhel}%{!?rhel:0} >= 5
Requires(post):		policycoreutils
Requires(postun):	policycoreutils
%if %{?fedora}%{!?fedora:0} >= 11 || %{?rhel}%{!?rhel:0} >= 6
Requires(post):		policycoreutils-python
Requires(postun):	policycoreutils-python
%endif
%endif

%description
The Berkeley Database Information Index (BDII) consists of a standard
LDAP database which is updated by an external process. The update process
obtains LDIF from a number of sources and merges them. It then compares
this to the contents of the database and creates an LDIF file of the
differences. This is then used to update the database.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}

chmod 644 %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%clean
rm -rf %{buildroot}

%pre
# Temp fix for upgrade from 5.2.5 to 5.2.7
service %{name} status > /dev/null 2>&1
if [ $? = 0 ]; then 
    touch /var/run/bdii/bdii.upgrade
    service %{name} stop > /dev/null 2>&1
fi

%post
sed "s/\(rootpw *\)secret/\1$(mkpasswd -s 0 | tr '/' 'x')/" \
    -i %{_sysconfdir}/%{name}/bdii-slapd.conf \
       %{_sysconfdir}/%{name}/bdii-top-slapd.conf

# Temp fix for upgrade from 5.2.5 to 5.2.7
if [ -f /var/run/bdii/bdii.upgrade ]; then
    rm -f /var/run/bdii/bdii.upgrade
    service %{name} start > /dev/null 2>&1
fi

/sbin/chkconfig --add %{name}

%if %{?fedora}%{!?fedora:0} >= 5 || %{?rhel}%{!?rhel:0} >= 5
semanage port -a -t ldap_port_t -p tcp 2170 2>/dev/null || :
semanage fcontext -a -t slapd_db_t "%{_localstatedir}/lib/%{name}/db(/.*)?" 2>/dev/null || :
semanage fcontext -a -t slapd_var_run_t "%{_localstatedir}/run/%{name}/db(/.*)?" 2>/dev/null || :
# Remove selinux labels for old bdii var dir
semanage fcontext -d -t slapd_db_t "%{_localstatedir}/run/%{name}(/.*)?" 2>/dev/null || :
%endif

%preun
if [ $1 -eq 0 ]; then
  service %{name} stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
  service %{name} condrestart > /dev/null 2>&1
fi
%if %{?fedora}%{!?fedora:0} >= 5 || %{?rhel}%{!?rhel:0} >= 5
if [ $1 -eq 0 ]; then
  semanage port -d -t ldap_port_t -p tcp 2170 2>/dev/null || :
  semanage fcontext -d -t slapd_db_t "%{_localstatedir}/lib/%{name}/db(/.*)?" 2>/dev/null || :
  semanage fcontext -d -t slapd_var_run_t "%{_localstatedir}/run/%{name}/db(/.*)?" 2>/dev/null || :
fi
%endif

%files
%defattr(-,root,root,-)
%attr(-,ldap,ldap) %{_localstatedir}/lib/%{name}
%attr(-,ldap,ldap) %{_localstatedir}/log/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/DB_CONFIG
%config(noreplace) %{_sysconfdir}/%{name}/DB_CONFIG_top
%config(noreplace) %{_sysconfdir}/%{name}/bdii.conf
%config(noreplace) %{_sysconfdir}/%{name}/BDII.schema
%attr(-,ldap,ldap) %config %{_sysconfdir}/%{name}/bdii-slapd.conf
%attr(-,ldap,ldap) %config %{_sysconfdir}/%{name}/bdii-top-slapd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_initrddir}/%{name}
%{_sbindir}/bdii-update
%{_mandir}/man1/bdii-update.1*
%doc copyright

%changelog
* Wed Jul 18 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 5.2.11-1
- BUG 95122: Created SLAPD_DB_DIR directoy with correct ownership if it doesn't exist
- BUG 95839: Added BDII_IPV6_SUPPORT

* Thu Mar 8 2012 Laurence Field <laurence.field@cern.ch> - 5.2.10-1
- New upsteam version that includes a new DB_CONFIG

* Tue Feb 8 2012 Laurence Field <laurence.field@cern.ch> - 5.2.9-1
- Fixed /var/run packaging issue

* Tue Feb 8 2012 Laurence Field <laurence.field@cern.ch> - 5.2.8-1
- Fixed a base64 encoding issue and added /var/run/bdii to the package

* Tue Feb 7 2012 Laurence Field <laurence.field@cern.ch> - 5.2.7-1
- Performance improvements to reduce memory and disk usage

* Wed Jan 25 2012 Laurence Field <laurence.field@cern.ch> - 5.2.6-1
- New upstream version that includes fedora patches and fix for EGI RT 3235

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Sep  4 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.2.5-1
- New upstream version 5.2.5

* Tue Jul 26 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.2.4-1
- New upstream version 5.2.4
- Drop patch accepted upstream: bdii-mdsvo.patch
- Move large files away from /var/run in order not to fill up /run partition

* Mon Jun 27 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.2.3-2
- Revert upstream hack that breaks ARC infosys

* Mon Jun 13 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.2.3-1
- New upstream version 5.2.3
- Drop patches accepted upstream: bdii-runuser.patch, bdii-context.patch,
  bdii-default.patch, bdii-shadowerr.patch, bdii-sysconfig.patch

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 01 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.1.13-1
- New upstream version 5.1.13
- Move restorecon from post sctiptlet to startup script in order to support
  /var/run on tmpfs

* Thu Sep 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.1.9-1
- New upstream version 5.1.9

* Thu Sep 02 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.1.8-1
- New upstream version 5.1.8

* Fri Jun 18 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.1.7-1
- New upstream version 5.1.7

* Sun May 23 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.1.5-1
- New upstream release 5.1.5
- Get rid of lsb initscript dependency

* Mon Apr 05 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.1.0-1
- New upstream verison 5.1.0
- Add SELinux context management to scriptlets

* Thu Mar 25 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0.8-4.460
- Update (svn revision 460)
- Use proper anonymous svn checkout instead of svnweb generated tarball

* Fri Feb 26 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0.8-3.443
- Update (svn revision 443)

* Wed Feb 24 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0.8-2.436
- Update (svn revision 436)

* Mon Feb 08 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 5.0.8-1.375
- Initial package (svn revision 375)
