Summary:	A caching nss module for disconnected operation
Name:		nss_updatedb
Version:	10
Release:	7
Group:		System/Libraries
License:	GPLv2
Url:		https://www.padl.com/
Source0:	http://www.padl.com/download/%{name}-%{version}.tar.gz
Source1:	nss_updatedb.cron
Source2:	nss_updatedb.sysconfig
# Uses getgrouplist(3) to find out the groups a user belongs to
# without enumerating all possible groups first
Source3:	getgrouplist.c
Patch0:		nss_updatedb-libdir.patch
Patch1:		nss_updatedb-automake-1.13.patch
Patch2:		nss_updatedb-4-key.patch
BuildRequires:	db_nss52-devel
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
%autopatch -p1
install -m 0644 %{SOURCE3} .
autoreconf -fi

%build
echo "#define DB_DIR \"/var/lib/misc\"" >> config.h.in
%configure2_5x

%make DEFS="-DHAVE_CONFIG_H -I/usr/include/db_nss"

%{__cc} %{optflags} -Werror getgrouplist.c -o getgrouplist

%install
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
%doc AUTHORS README ChangeLog
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/nss_updatedb*
%{_bindir}/getgrouplist
%{_sysconfdir}/cron*/*
%{_mandir}/man8/nss_updatedb.8*

