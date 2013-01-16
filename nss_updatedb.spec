%{!?mdkversion: %define notmdk 1}

Summary: 	A caching nss module for disconnected operation
Name:      	nss_updatedb
Version:   	10
Release:   	5
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
Patch1:		nss_updatedb-automake-1.13.patch
Patch2:		nss_updatedb-4-key.patch
%if %{?notmdk:1}%{?!notmdk:0}
BuildRequires:	db4-devel >= 4.0
%else
BuildRequires:	db_nss-devel >= 4.2.52-5mdk
%endif
BuildRequires:	automake
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
%apply_patches
install -m 0644 %{SOURCE3} .

%build
autoreconf -fi

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,755)
%doc AUTHORS README ChangeLog
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/nss_updatedb*
%{_bindir}/getgrouplist
%{_sysconfdir}/cron*/*
%{_mandir}/man8/nss_updatedb.8*


%changelog
* Sun May 15 2011 Oden Eriksson <oeriksson@mandriva.com> 10-1mdv2011.0
+ Revision: 674854
- 10
- rediff patches and drop one
- mass rebuild

* Wed Oct 27 2010 Luca Berra <bluca@mandriva.org> 8-7mdv2011.0
+ Revision: 589562
- really fix DB_LOG_AUTO_REMOVE (mdv#61306)

* Tue Oct 26 2010 Luca Berra <bluca@mandriva.org> 8-6mdv2011.0
+ Revision: 589536
+ rebuild (emptylog)

* Tue Oct 26 2010 Luca Berra <bluca@mandriva.org> 8-5mdv2011.0
+ Revision: 589535
- fix DB_LOG_AUTO_REMOVE not working (mdv#61306)

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 8-5mdv2010.1
+ Revision: 520196
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 8-4mdv2010.0
+ Revision: 426259
- rebuild

* Fri Apr 10 2009 Luca Berra <bluca@mandriva.org> 8-3mdv2009.1
+ Revision: 365849
- fix building with bdb 4.7
- workaround for broken drakauth (#49769)
  ignore some other possible fixed databases in cron job

* Tue Mar 18 2008 Oden Eriksson <oeriksson@mandriva.com> 8-2mdv2008.1
+ Revision: 188540
- fix #39033 (nss_updatedb hardcoded LIBNSS_DIR to /lib instead of /lib64)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Oct 29 2007 Buchan Milne <bgmilne@mandriva.org> 8-1mdv2008.1
+ Revision: 103449
- New version 8


* Fri Nov 17 2006 Andreas Hasenack <andreas@mandriva.com> 7-2mdv2007.0
+ Revision: 85283
- tabs
- use getgrouplist(3) to get groups instead of "id", which
  enumerates all groups and is expensive if group info is
  stored in, for example, LDAP

* Fri Nov 17 2006 Andreas Hasenack <andreas@mandriva.com> 7-1mdv2007.1
+ Revision: 85127
- updated to version 7, fixing a segfault
- bunzipped patches
- added Frederic Lepied <flepied@mandriva.com> modifications to
  only fetch information from logged in users
- changed above modifications to cope better with group with spaces
  in their names (like "Domain Users")
- return correct errorlevel on end to avoid cron spamming
- Import nss_updatedb

* Tue Jun 13 2006 Buchan Milne <bgmilne@mandriva.org> 6-1mdv2007.0
- new version 6
- integrate changes from bug #19461
- drop pre-%%mkrel macros
- integrate changes to build on non-mandriva systems (with compat macros)

* Thu Oct 27 2005 Pierre Palatin <pierre@palats.com> 4-2mdk
- Patch for x86_64

* Tue Jul 12 2005 Buchan Milne <bgmilne@linux-mandrake.com> 4-1mdk
- New release 4

* Fri Dec 10 2004 Buchan Milne <bgmilne@linux-mandrake.com> 3-1mdk
- version 3
- drop all patches (merged upstream except for dbpath which can 
  now be set via config.h)
- add cron script (S1) and a config file for it (S2)

* Wed Dec 08 2004 Buchan Milne <bgmilne@linux-mandrake.com> 1-1mdk
- use correct version number
- use transactions (p0)
- distribution-specific release tag

* Tue Aug 17 2004 Luca Berra <bluca@vodka.it> 0.1-2mdk 
- rebuilt with db-4.2

* Tue Mar 02 2004 Luca Berra <bluca@vodka.it> 0.1-1mdk 
- initial mandrake contrib

