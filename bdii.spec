%define metadata config
%define name %( grep NAME %{metadata} | sed 's/^[^:]*: //' )
%define version %( grep VERSION %{metadata} | sed 's/^[^:]*: //' )
%define release %( grep RELEASE %{metadata} | sed 's/^[^:]*: //' )
%define prefix %( grep PREFIX %{metadata} | sed 's/^[^:]*: //' )
%define license %( grep LICENSE %{metadata} | sed 's/^[^:]*: //' )
%define vendor %( grep VENDOR %{metadata} | sed 's/^[^:]*: //' )
%define packager %( grep PACKAGER %{metadata} | sed 's/^[^:]*: //' )
%define group %( grep GROUP %{metadata} | sed 's/^[^:]*: //' )
%define desc %( grep DESCRIPTION %{metadata} | sed 's/^[^:]*: //' )

Summary: %{name}
Name: %{name}
Version: %{version}
Vendor: %{vendor}
Release: %{release}
License: %{license}
Group: %{group}
Source: %{name}-%{version}.src.tgz
BuildArch: noarch
Prefix: %{prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Packager: %{packager}

%description
%{desc}
%prep

%setup -c

%build
make install prefix=%{buildroot}%{prefix}

%post

%preun

%postun

%files -f INSTALLED_FILES
%defattr(-,root,root)

%clean
rm -rf %{buildroot}
