Summary:	Allows to monitor UPS Active Power
Summary(pl):	Narzêdzia do monitorowania UPS-ów Active Power
Name:		upsmonitor
Version:	1.0.9
Release:	1
License:	Free
Vendor:		Artur Miarecki (MAYANET) artur.miarecki@mayanet.pl
Group:		Daemons
Requires:	/bin/mail
Source0:	http://download.mayanet.pl/ups_monitor/arch/1.0.9/upsmonitor.pl
Source1:	http://download.mayanet.pl/ups_monitor/arch/1.0.9/upsmonitor.conf
Source2:	http://download.mayanet.pl/ups_monitor/historia.txt
Source10:	%{name}-readme.txt
# http://download.mayanet.pl/ups_monitor/readme.txt
Source11:	%{name}.init
URL:		http://download.mayanet.pl/ups_monitor/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allows to monitor UPS Active Power and safely shutdown system.

%description -l pl
Narzêdzia pozwalaj±ce na monitorowanie i bezpieczne zamkniêcie systemu
operacyjnego komputera z do³±czonym zasilaczem UPS Active Power.

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
if [ -f /var/lock/subsys/upsmonitor ]; then
	/etc/rc.d/init.d/upsmonitor restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/upsmoinitor start\" to start ups_monitor."
fi

%files 
%defattr(644,root,root,755)
%doc readme.txt historia.txt
%attr(750,root,root) %{_sbindir}/upsmonitor.pl
%attr(754,root,root) /etc/rc.d/init.d/upsmonitor
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/upsmonitor.conf
