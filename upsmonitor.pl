#!/usr/bin/perl


# Monitorowanie UPS Active Power 600
# by Artur Miarecki, MAYANET, artur.miarecki@mayanet.pl
# 2004-05-01
# wersja 1.0.7
# freeware

$cfg_serialport="/dev/ttyS0";
$cfg_interval=10;	# sekund
$cfg_laststatefile="/var/log/ups.state";
$cfg_logfile="/var/log/ups.log";
$cfg_datlogfile="/var/log/ups.dat";
$cfg_emaile="jakisadres\@jakisserwer.pl";  # Uwaga! przypominam o backslash'owaniu znaku "@"!
$cfg_maxupstime=3;   # minut
$cfg_logujstatusy=1;    # logowanie statusu UPS (1=ON, 0=off)


use Device::SerialPort;


sub odczytaj_czas {
    # Odczytaj biezacy czas
    ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime(time());
    $year+=1900;
    $mon++;
    $year=sprintf("%04d",$year);
    $mon=sprintf("%02d",$mon);
    $mday=sprintf("%02d",$mday);
    $hour=sprintf("%02d",$hour);
    $min=sprintf("%02d",$min);
    $sec=sprintf("%02d",$sec);
    $dt="$year-$mon-$mday $hour:$min:$sec";

    return($dt);
};


sub zapisz_do_logu {
    my $txt=shift @_;

    $dt=odczytaj_czas();
    open (FL, ">>$cfg_logfile");
    print FL "$dt\t$txt\n";
    close (FL);
}


sub zapisz_do_datlogu {
    my $txt=shift @_;

    $dt=odczytaj_czas();
    open (FLD, ">>$cfg_datlogfile");
    print FLD "$dt\t$txt\n";
    close (FLD);
}


sub alert {
    my $txt=shift @_;

    `/bin/mail -s"$txt" $cfg_emaile </dev/null`;
}



# Start - uruchom sie w tle
if (!defined($child_pid=fork())) {
    die "UPS MONITOR - nie moge uruchomic sie w tle!";
} elsif ($child_pid) {
    print "UPS MONITOR - uruchomiony w tle (PID=$child_pid)\n";
} else {

    zapisz_do_logu("Start monitorowania UPS");
    alert("Start monitorowania UPS");

    $maxupstime_n=int($cfg_maxupstime*60/$cfg_interval);

	# Zapisz startowy stan UPS
	open (F, ">$cfg_laststatefile");
	print F "1\n";
	print F "0\n";
	close (F);

    while (1) {

	# Skonfiguruj lacze szeregowe
	$port = new Device::SerialPort($cfg_serialport);
	$port->baudrate(2400);
	$port->parity("none");
	$port->databits(8);
	$port->stopbits(1);
	$port->handshake("none");
	$port->read_const_time(2000);
	$port->write_settings;


	# Odczytaj ostatni stan UPS
	open (F, "$cfg_laststatefile");
	$laststate=<F>;
	chop $laststate;
	$timeonups=<F>;
	chop $timeonups;
	close (F);
	$laststate+=0;
	$timeonups+=0;


	# Wyslij rozkaz odczytu statusu UPS
	$port->pulse_break_on(200);
	$port->lookclear;
	$port->write("\rQ1\r");



	# Odczytaj status UPS
	for ($i=0;$i<100;$i++) { $upsstatustab[$i]=""; }
	$i=0;
	$buf="";
	while (1) {
	    ($n,$c)=$port->read(1);
	    if ($n eq 0 || $c eq "(") { last; }
	}
	while (1) {
	    ($n,$c)=$port->read(1);
	    if (ord($c) eq 13) { last; }
	    $buf.=$c;
	    if ($c eq " ") { $i++; next; }
	    $upsstatustab[$i].=$c;
	}
	undef $port;


	# Zinterpretuj biezacy stan UPS
	if (int($upsstatustab[0]) eq 0
	    && int($upsstatustab[1]) eq 0
	    && substr($upsstatustab[7],0,1) eq "1"
	) {
	    $currentstate=0;
	    $timeonups++;
	} else {
	    $currentstate=1;
	    $timeonups=0;
	}
	$batterylow=substr($upsstatustab[7],1,1)+0;



	# Zapisz do logu ew zmiany stanu
	if ($laststate ne $currentstate) {
	    if ($currentstate eq 0) {
		zapisz_do_logu("Zanik zasilania!");
		alert("Zanik zasilania!");
	    } else {
		zapisz_do_logu("Powrot zasilania.");
		alert("Powrot zasilania.");
	    }
	}
	$down=0;
	if ($timeonups >= $maxupstime_n) {
	    zapisz_do_logu("Shutdown-zanik zasilania>".$cfg_maxupstime."min.");
	    alert("Shutdown-zanik zasilania>".$cfg_maxupstime."min.");
	    $down=1;
	    $currentstate=0;
	}
	if ($batterylow eq 1) {
	    zapisz_do_logu("Shutdown-battery low.");
	    alert("Shutdown-battery low.");
	    $down=1;
	    $currentstate=0;
	}



	# Zapisz biezacy stan UPS
	open (F, ">$cfg_laststatefile");
	print F "$currentstate\n";
	print F "$timeonups\n";
	close (F);



	# Sprawdz czy shutdown systemu
	if ($down eq 1) {
	    sleep 5;
	    `/sbin/init 0`;
	}

	if ($cfg_logujstatusy eq 1) {
	    zapisz_do_datlogu ("$buf");
	}

	sleep $cfg_interval;

    }
}
