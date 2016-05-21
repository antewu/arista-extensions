Summary: BIRD Internet Routing Daemon
Name: bird
Version: 1.6.0
Release: 1
License: GPL
Group: Networking/Daemons
Source: https://github.com/BIRD/bird/archive/v%{version}.tar.gz
Source1: birdc6
Buildroot: /var/tmp/bird-root
Url: http://bird.network.cz
Requires: /sbin/chkconfig
BuildRequires: readline-devel ncurses-devel flex bison autoconf gcc make

%description
BIRD is dynamic routing daemon supporting IPv4 and IPv6 versions of routing
protocols BGP, RIP and OSPF.

%prep
%setup -n bird-%{version}

%build
autoconf
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --enable-ipv6
make
mv bird bird6
mv birdc birdc6

make clean
autoconf
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var
make


%install
rm -rf $RPM_BUILD_ROOT/*

make install prefix=$RPM_BUILD_ROOT/usr sysconfdir=$RPM_BUILD_ROOT/etc localstatedir=$RPM_BUILD_ROOT/var

install birdc6 $RPM_BUILD_ROOT/usr/sbin
install bird6 $RPM_BUILD_ROOT/usr/sbin
install birdcl $RPM_BUILD_ROOT/usr/sbin
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/mnt/flash/bird
install $RPM_BUILD_DIR/bird-%{version}/misc/bird.init $RPM_BUILD_ROOT/etc/rc.d/init.d/bird
install bird.conf $RPM_BUILD_ROOT/mnt/flash/bird

%post
/sbin/ldconfig
/sbin/chkconfig --add bird
ln -s /mnt/flash/bird/bird.conf /etc/bird.conf

%preun
if [ $1 = 0 ] ; then
        /sbin/chkconfig --del bird
fi

%files
%attr(755,root,root) /usr/sbin/bird
%attr(755,root,root) /usr/sbin/bird6
%attr(755,root,root) /usr/sbin/birdc
%attr(755,root,root) /usr/sbin/birdc6
%attr(755,root,root) /usr/sbin/birdcl
%attr(755,root,root) /etc/rc.d/init.d/bird
%attr(644,admin,admin) /mnt/flash/bird/bird.conf
%attr(644,admin,admin) /etc/bird.conf