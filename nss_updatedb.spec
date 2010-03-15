%define	name nss_updatedb
%define	version	8
%define rel 5

%{!?mdkversion: %define notmdk 1}

Summary: 	A caching nss module for disconnected operation
Name:      	%{name}
Version:   	%{version}
Release:   	%mkrel %rel
Source: 	http://www.padl.com/download/%{name}-%{version}.tar.gz
Source1:	nss_updatedb.cron
Source2:	nss_updatedb.sysconfig
# Uses getgrouplist(3) to find out the groups a user belongs to
# without enumerating all possible groups first
Source3:	getgrouplist.c
Patch0:		nss_updatedb-libdir.patch
Patch1:		nss_updatedb-3-autologremove.patch
Patch2:		nss_updatedb-4-key.patch
Group:		System/Libraries
License:	GPL
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot
%if %{?notmdk:1}%{?!notmdk:0}
BuildRequires:	db4-devel >= 4.0
%else
BuildRequires:	db_nss-devel >= 4.2.52-5mdk
%endif
BuildRequires:	automake1.4
Url:		http://www.padl.com/
Requires:	nss_db

%description
The nss_updatedb utility maintains a local cache of network
directory user and group information.
Used in conjunction with the pam_ccreds module, it provides
a mechanism for disconnected use of network directories.
These tools are designed to work with pam_ldap and nss_ldap,
also available from PADL.

%prep
%setup -q
%patch0 -p1 -b .libdir
%patch1 -p1 -b .autologremove
%patch2 -p1 -b .key
install -m 0644 %{SOURCE3} .

%build
autoreconf

%if %{?!notmdk:1}%{?notmdk:0}
echo "#define DB_DIR \"/var/lib/misc\"" >> config.h.in
%endif
echo "#define LIBNSS_DIR \"/%{_lib}\"" >> config.h.in

%configure2_5x

%make %{?!notmdk:DEFS="-DHAVE_CONFIG_H -I/usr/include/db_nss"}

gcc %{optflags} -Werror getgrouplist.c -o getgrouplist

%install
rm -rf %{buildroot}
%makeinstall

install -m 755 %{SOURCE1} %{buildroot}/%{_sbindir}

install -d %{buildroot}/%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

install -d %{buildroot}/%{_sysconfdir}/cron.{monthly,weekly,daily,hourly}
for i in monthly weekly daily hourly
do ln -s %{_sbindir}/%{name}.cron %{buildroot}/%{_sysconfdir}/cron.${i}/%{name}
done

mkdir %{buildroot}%{_bindir}
install -m 0755 getgrouplist %{buildroot}%{_bindir}

%files
%defattr(-,root,root,755)
%doc AUTHORS README ChangeLog
%{_sbindir}/nss_updatedb*
%{_bindir}/getgrouplist
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/cron*/*

%clean
rm -rf %{buildroot}



