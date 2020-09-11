%bcond_without rust
%global __requires_exclude ^libdnf[.]so[.].*$
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$

Name:		rpm-ostree
Version:	2018.8
Release:	2
Summary:	Hybrid image/package system
License:	LGPLv2+
URL:		https://github.com/projectatomic/rpm-ostree
Source0:	https://github.com/coreos/rpm-ostree/archive/v%{version}.tar.xz#/%{name}-%{version}.tar.xz 

Patch0:         eliminate-rpmostree-differences.patch

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
BuildRequires:   pkgconfig(libsolv)

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
%define _configure %{?rusttoolset} ./configure
%configure --disable-silent-rules --enable-gtk-doc \
           %{?with_rust:--enable-rust}

%{?rusttoolset} %make_build

%install
%{?rusttoolset}  %make_install 
%delete_la 

%files
%defattr(-,root,root)
%doc README.md
%license COPYING
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
* Sat Oct 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 2018.8-2
- Package init
