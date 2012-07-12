%define _lib lib
%define upstreamname libogg

Name:		somis-libogg
Version:	1.3.0
Release:	0..1
Summary:	Ogg Bitstream Library.

Group:		System Environment/Libraries
License:	BSD
URL:		http://www..org/
Vendor:		Xiph.org Foundation <team@.org>
Source:		http://www.vorbis.com/files/1.0.1/unix/%{upstreamname}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

# We're forced to use an epoch since both Red Hat and Ximian use it in their
# rc packages
Epoch:		2
# Dirty trick to tell rpm that this package actually provides what the
# last rc and beta was offering
Provides:	%{name} = 1.3.0

%description
Libogg is a library for manipulating ogg bitstreams.  It handles
both making ogg bitstreams and getting packets from ogg bitstreams.

%package devel
Summary: 	Ogg Bitstream Library Development
Group: 		Development/Libraries
Requires: 	somis-libogg = %{version}
# Dirty trick to tell rpm that this package actually provides what the
# last rc and beta was offering
Provides:	%{name}-devel = 1.3.0

%description devel
The libogg-devel package contains the header files, static libraries
and documentation needed to develop applications with libogg.

%prep
%setup -q -n %{upstreamname}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} --enable-static --enable-shared
make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES COPYING README
%{_libdir}/libogg.so.*

%files devel
%defattr(-,root,root)
%doc %{_docdir}/libogg-%{version}/ogg/*.html
%doc %{_docdir}/libogg-%{version}/ogg/*.css
%doc %{_docdir}/libogg-%{version}/*.html
%doc %{_docdir}/libogg-%{version}/*.txt
%doc %{_docdir}/libogg-%{version}/*.png
%dir %{_includedir}/ogg
%{_includedir}/ogg/ogg.h
%{_includedir}/ogg/os_types.h
%{_includedir}/ogg/config_types.h
%{_libdir}/libogg.a
%{_libdir}/libogg.la
%{_libdir}/libogg.so
%{_libdir}/pkgconfig/ogg.pc
%{_datadir}/aclocal/ogg.m4

%changelog
* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of spec file.
