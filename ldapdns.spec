Summary:	DNS server that pulls data from an LDAP directory
Name:		ldapdns
Version:	2.06
Release:	%mkrel 7
License:	GPL
Group:		System/Servers
URL:		https://www.nimh.org/
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-init.bz2
Source2:	%{name}-syscfg.bz2
Source3:	%{name}-ldif.bz2
Source4:	%{name}.conf.bz2
Patch0:		ldapdns-2.06-label_at_end_of_compound_statement.diff
Requires:	openldap
Requires:	openssl
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	openldap-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
LDAPDNS is a ultra-fast, stable, multithreaded DNS server that
pulls data from an LDAP directory. It supports RFC1279 
(bind-style), Microsoft Active Directory, and it's own directory
layouts.

#%package admin
#Summary:	Administrative utilities for ldapdns
#Group:		System/Servers
#Requires:	perl-Crypt-SSLeay
#Requires:	perl-ldap
#Prereq:		ldapdns = %{version}
#
#%description admin
#This package contains administrative utilities for ldapdns written
#in perl.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0

%build

perl -pi -e "s|/usr/local|%{_prefix}|g" configure
CFLAGS="%{optflags}" ./configure --prefix=%{_prefix}
make 

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_datadir}/ldapdns

RUN_USER=root FORCE_INITRC=1 NO_DAEMONTOOLS=1 NO_TCPSERVERS=1 \
  INITRC=1 bin=sbin DESTDIR=%{buildroot} prefix=%{_prefix} ./install.sh

bzcat %{SOURCE1} > %{buildroot}%{_initrddir}/ldapdns
chmod 755 %{buildroot}%{_initrddir}/ldapdns

bzcat %{SOURCE2} > %{buildroot}%{_sysconfdir}/sysconfig/ldapdns
chmod 644 %{buildroot}%{_sysconfdir}/sysconfig/ldapdns

bzcat %{SOURCE4} > %{buildroot}%{_sysconfdir}/ldapdns.conf
chmod 644 %{buildroot}%{_sysconfdir}/ldapdns.conf

bzcat %{SOURCE3} > ldapdns-sample.ldif

touch %{buildroot}%{_var}/lib/ldapdns/password

# Remove installed but not packaged files
rm -rf %{buildroot}/etc/init.d

# install the admin stuff... (djb stuff...)
install -m755 admin/* %{buildroot}%{_datadir}/ldapdns/
install -m755 ldapaxfr-conf %{buildroot}%{_datadir}/ldapdns/
install -m755 ldapdns-conf %{buildroot}%{_datadir}/ldapdns/

# make strip work
chmod 755 %{buildroot}%{_sbindir}/*

%pre
%_pre_useradd ldapdns /var/lib/ldapdns /bin/false

%post
RUN_UID=`id -u ldapdns`
RUN_GID=`id -g ldapdns`
perl -pi -e "s|^RUN_UID=.*|RUN_UID=$RUN_UID|g" %{_sysconfdir}/ldapdns.conf
perl -pi -e "s|^RUN_GID=.*|RUN_GID=$RUN_GID|g" %{_sysconfdir}/ldapdns.conf
%_post_service ldapdns

%preun
%_preun_service ldapdns

%postun
%_postun_userdel ldapdns

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS CHANGELOG FAQ INSTALL MANIFEST TODO VERSIONS ldapdns-sample.ldif
%doc README README.axfr README.comparison README.configure README.generic-rr 
%doc README.how-can-i-help README.quotes README.search
%attr(0755,root,root) %{_initrddir}/ldapdns
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/ldapdns
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ldapdns.conf
%attr(0755,ldapdns,ldapdns) %dir %{_localstatedir}/lib/ldapdns
%attr(0640,ldapdns,ldapdns) %config(noreplace) %{_localstatedir}/lib/ldapdns/password
%attr(0600,ldapdns,ldapdns) %{_localstatedir}/lib/ldapdns/axfr
%attr(0755,root,root) %{_sbindir}/ldapdns
%attr(0755,root,root) %{_sbindir}/ldapaxfr

#%files admin
#%defattr(-,root,root)
%doc README.admin
%attr(0755,root,root) %{_datadir}/ldapdns/add_basic_zone
%attr(0755,root,root) %{_datadir}/ldapdns/add_generic_record
%attr(0755,root,root) %{_datadir}/ldapdns/add_sub_alias
%attr(0755,root,root) %{_datadir}/ldapdns/add_sub_host
%attr(0755,root,root) %{_datadir}/ldapdns/add_sub_mx
%attr(0755,root,root) %{_datadir}/ldapdns/config.pl
%attr(0755,root,root) %{_datadir}/ldapdns/dhcp_names
%attr(0755,root,root) %{_datadir}/ldapdns/samba_names
%attr(0755,root,root) %{_datadir}/ldapdns/secondary_zone
%attr(0755,root,root) %{_datadir}/ldapdns/set_generic_record
%attr(0755,root,root) %{_datadir}/ldapdns/set_ip_pointer
%attr(0755,root,root) %{_datadir}/ldapdns/set_sub_alias
%attr(0755,root,root) %{_datadir}/ldapdns/set_sub_host
%attr(0755,root,root) %{_datadir}/ldapdns/set_sub_mx
%attr(0755,root,root) %{_datadir}/ldapdns/set_txt
%attr(0755,root,root) %{_datadir}/ldapdns/transfer_zone
%attr(0755,root,root) %{_datadir}/ldapdns/unset_ip_pointer
%attr(0755,root,root) %{_datadir}/ldapdns/ldapaxfr-conf
%attr(0755,root,root) %{_datadir}/ldapdns/ldapdns-conf


