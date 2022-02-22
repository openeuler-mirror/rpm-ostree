%bcond_without rust
%global __requires_exclude ^libdnf[.]so[.].*$
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$

Name:		rpm-ostree
Version:	2022.1
Release:	1
Summary:	Hybrid image/package system
License:	LGPLv2+
URL:		https://github.com/projectatomic/rpm-ostree
Source0:	https://github.com/coreos/rpm-ostree/archive/v%{version}.tar.xz#/%{name}-%{version}.tar.xz 

%if %{with rust}

%if !%{defined rust_arches}
%define rust_arches x86_64 i686 armv7hl aarch64 ppc64 ppc64le s390x
%endif 

ExclusiveArch: %{rust_arches}

%if %{defined rusttoolset_version}
BuildRequires: %{rusttoolset_version}-cargo
%else
BuildRequires:	 cargo 
%endif

%endif

BuildRequires:   /usr/bin/python3 autoconf automake libtool git chrpath libattr-devel 
BuildRequires:   gtk-doc gperf gnome-common /usr/bin/g-ir-scanner ostree-devel cmake
BuildRequires:   polkit-devel json-glib-devel rpm-devel libarchive-devel systemd-devel 
BuildRequires:   libcap-devel libcurl-devel librepo-devel expat-devel check-devel 
BuildRequires:   pkgconfig(libsolv) gcc gcc-c++
BuildRequires:   chrpath json-c-devel libmodulemd-devel sqlite-devel cppunit-devel
BuildRequires:   glib2-devel gpgme-devel libsolv-tools make python3-devel python3-sphinx swig libsmartcols-devel

Requires:	 ostree bubblewrap fuse 

Provides:        rpm-ostree-libs = %{version}-%{release}
Obsoletes:       rpm-ostree-libs < %{version}-%{release}

%description
rpm-ostree is a hybrid image/package system.  It supports
"composing" packages on a build server into an OSTree repository,
which can then be replicated by client systems with atomic upgrades.
Additionally, unlike many "pure" image systems, with rpm-ostree
each client system can layer on additional packages, providing
a "best of both worlds" approach.

%package         devel
Summary:         Header files for rpm-ostree
Requires:        %{name} = %{version}-%{release}

%description     devel
Header files for rpm-ostree.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
%{?rusttoolset} env NOCONFIGURE=1 ./autogen.sh
%configure --disable-silent-rules --enable-gtk-doc \
           %{?with_rust:--enable-rust}

%{?rusttoolset} %make_build

%install
%{?rusttoolset}  %make_install 
%delete_la 

chrpath -d %{buildroot}%{_libdir}/librpmostree-1.so.1.0.0
chrpath -d %{buildroot}%{_bindir}/rpm-ostree

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}/%{name}" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

%ldconfig_scriptlets

install -d -m 0755 %{buildroot}/etc/dbus-1/system.d/
install -pm 0644 src/daemon/org.projectatomic.rpmostree1.conf %{buildroot}/etc/dbus-1/system.d/

%files
%defattr(-,root,root)
%doc README.md
%license COPYING.*
%{_bindir}/*
%{_sysconfdir}/dbus-1/system.d/*
%{_sysconfdir}/rpm-ostreed.conf
%{_libdir}/*.so.*
%{_libdir}/rpm-ostree/*
%{_libdir}/girepository-1.0/*
%{_libexecdir}/rpm-ostree*
%{_prefix}/lib/systemd/system/*
%{_datadir}/dbus-1/system-services
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system.d/org.projectatomic.rpmostree1.conf
%{_datadir}/bash-completion/completions/rpm-ostree
%config(noreplace) /etc/ld.so.conf.d/*

%files       devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/*
%{_datadir}/gir-1.0/*-1.0.gir
%{_datadir}/dbus-1/interfaces/org.projectatomic.rpmostree1.xml

%files       help
%defattr(-,root,root)
%{_mandir}/man*/*

%changelog
* Wed Jan 19 2022 SimpleUpdate Robot <tc@openeuler.org> - 2022.1-1
- Upgrade to version 2022.1

* Fri Sep 10 2021 gaihuiying <gaihuiying1@huawei.com> - 2018.8-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove rpath of rpm-ostree's binary files

* Mon May 31 2021 huanghaitao <huanghaitao8@huawei.com> - 2018.8-3
- Completing build dependencies to fix gcc/gcc-c++ compiler missing error

* Sat Oct 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 2018.8-2
- Package init
