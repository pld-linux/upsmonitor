Summary:	Allows to monitor UPS Active Power
Summary(pl.UTF-8):   Narzędzia do monitorowania UPS-ów Active Power
Name:		upsmonitor
Version:	1.0.11
Release:	1
License:	Free
Group:		Daemons
Source0:	http://download.mayanet.pl/ups_monitor/arch/%{version}/%{name}.pl
Source1:	http://download.mayanet.pl/ups_monitor/arch/%{version}/%{name}.conf
Source2:	http://download.mayanet.pl/ups_monitor/historia.txt
# http://download.mayanet.pl/ups_monitor/readme.txt
Source10:	%{name}-readme.txt
Source11:	%{name}.init
URL:		http://download.mayanet.pl/ups_monitor/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	/bin/mail
Requires:	rc-scripts
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allows to monitor UPS Active Power and safely shutdown system.

%description -l pl.UTF-8
Narzędzia pozwalające na monitorowanie i bezpieczne zamknięcie systemu
operacyjnego komputera z dołączonym zasilaczem UPS Active Power.

%prep
%setup -q -c -T
install %{SOURCE10} readme.txt
install %{SOURCE2} historia.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/scripts,/etc/rc.d/init.d,/var/log}

install %{SOURCE11} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsmonitor
install %{SOURCE0} $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/upsmonitor.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add upsmonitor
%service upsmonitor restart "ups_monitor"

%preun
if [ "$1" = "0" ]; then
	%service upsmonitor stop
	/sbin/chkconfig --del upsmonitor
fi

%files
%defattr(644,root,root,755)
%doc readme.txt historia.txt
%attr(750,root,root) %{_sbindir}/upsmonitor.pl
%attr(754,root,root) /etc/rc.d/init.d/upsmonitor
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/upsmonitor.conf
