Summary: 	A caching nss module for disconnected operation
Name:      	nss_updatedb
Version:   	10
Release:   	2
Group:		System/Libraries
License:	GPL
URL:		http://www.padl.com/
Source0: 	http://www.padl.com/download/%{name}-%{version}.tar.gz
Source1:	nss_updatedb.cron
Source2:	nss_updatedb.sysconfig
# Uses getgrouplist(3) to find out the groups a user belongs to
# without enumerating all possible groups first
Source3:	getgrouplist.c
Patch0:		nss_updatedb-libdir.patch
Patch2:		nss_updatedb-4-key.patch
BuildRequires:	db_nss-devel >= 4.2.52-5mdk
BuildRequires:	automake1.4
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
%patch0 -p1 -b .libdir~
%patch2 -p1 -b .key~
cp %{SOURCE3} .
autoreconf -fi

%build
echo "#define LIBNSS_DIR \"/%{_lib}\"" >> config.h.in

%configure2_5x
%make

gcc %{optflags} -Werror getgrouplist.c -o getgrouplist

%install
%makeinstall

install -m755 %{SOURCE1} -D %{buildroot}%{_sbindir}/nss_updatedb.cron
install -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m755 getgrouplist -D %{buildroot}%{_bindir}/getgrouplist

install -d %{buildroot}%{_sysconfdir}/cron.{monthly,weekly,daily,hourly}
for i in monthly weekly daily hourly; do
	ln -s %{_sbindir}/%{name}.cron %{buildroot}%{_sysconfdir}/cron.${i}/%{name}
done

%files
%doc AUTHORS README ChangeLog
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/nss_updatedb*
%{_bindir}/getgrouplist
%{_sysconfdir}/cron*/*
%{_mandir}/man8/nss_updatedb.8*
