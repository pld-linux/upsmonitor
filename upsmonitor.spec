Summary:	Allows to monitor UPS Active Power
Summary(pl):	Narzêdzia do monitorowania UPS-ów Active Power
Name:		upsmonitor
Version:	1
Release:	0.1
License:	Free
Group:		Daemons
Source0:	http://download.mayanet.pl/ups_monitor/upsmonitor.pl
Source1:	%{name}-readme.txt
# http://download.mayanet.pl/ups_monitor/readme.txt
Source2:	%{name}.init
Vendor:	  Artur Miarecki (MAYANET)  artur.miarecki@mayanet.pl
URL:		http://download.mayanet.pl/ups_monitor/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allows to monitor UPS Active Power and safely shutdown system.

%description -l pl
Narzêdzia pozwalaj±ce na monitorowanie i bezpieczne zamkniêcie systemu
operacyjnego komputera z do³±czonym zasilaczem UPS Active Power.

%prep

rm -rf %{name}
mkdir %{name}
install %{SOURCE1} readme.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/scripts,/etc/rc.d/init.d,/var/log}

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/upsmonitor
install %{SOURCE0} $RPM_BUILD_ROOT/%{_sbindir}

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
%doc readme.txt
%attr(750,root,root) %{_sbindir}/upsmonitor.pl
%attr(754,root,root) /etc/rc.d/init.d/upsmonitor
