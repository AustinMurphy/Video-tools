# SOMIS defs:
%define upstreamname libvorbis
%define name somis-libvorbis

#vorbis has chosen to include /redhat in the topdir path. This is the fix
%define _topdir	/home/kbende/rpmbuild

Name:		somis-libvorbis
Version:	1.3.3
Release:	0..1
Summary:	The Vorbis General Audio Compression Codec.

Group:		System Environment/Libraries
License:	BSD
URL:		http://www..org/
Vendor:		Xiph.org Foundation <team@.org>
Source:		%{upstreamname}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Conflicts:	libvorbis

# We're forced to use an epoch since both Red Hat and Ximian use it in their
# rc packages
#Epoch:          2
# Dirty trick to tell rpm that this package actually provides what the
# last rc and beta was offering
Provides:       %{name} = %{version}
#Provides:       %{name} = %{epoch}:1.0beta4-%{release}

Requires:	somis-libogg >= 1.1
BuildRequires:	somis-libogg-devel >= 1.1

%description
Ogg Vorbis is a fully open, non-proprietary, patent-and-royalty-free,
general-purpose compressed audio format for audio and music at fixed 
and variable bitrates from 16 to 128 kbps/channel.

%package devel
Summary: 	Vorbis Library Development
Group: 		Development/Libraries
Requires:	somis-libogg-devel >= 1.1
Requires:	somis-libvorbis = %{version}
# Dirty trick to tell rpm that this package actually provides what the
# last rc and beta was offering
Provides:       %{upstreamname}-devel = %{version}
#Provides:       %{upstreamname}-devel = %{epoch}:1.0beta4-%{release}

%description devel
The libvorbis-devel package contains the header files, static libraries 
and documentation needed to develop applications with libvorbis.

%prep
%setup -q -n %{upstreamname}-%{version}
./autogen.sh

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} --enable-static --libdir=/usr/lib64
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
%doc AUTHORS COPYING README
%{_libdir}/libvorbis.so.*
%{_libdir}/libvorbisfile.so.*
%{_libdir}/libvorbisenc.so.*

%files devel
%doc %{_docdir}/libvorbis-1.3.3/*.html
%doc %{_docdir}/libvorbis-1.3.3/*.png
%doc %{_docdir}/libvorbis-1.3.3/*.txt
%doc %{_docdir}/libvorbis-1.3.3/*.stamp
%doc %{_docdir}/libvorbis-1.3.3/*.xml
%doc %{_docdir}/libvorbis-1.3.3/vorbisfile
%doc %{_docdir}/libvorbis-1.3.3/vorbisenc
%doc %{_docdir}/libvorbis-1.3.3/libvorbis
%{_datadir}/aclocal/vorbis.m4
%dir %{_includedir}/vorbis
%{_includedir}/vorbis/codec.h
%{_includedir}/vorbis/vorbisfile.h
%{_includedir}/vorbis/vorbisenc.h
%{_libdir}/libvorbis.a
%{_libdir}/libvorbis.la
%{_libdir}/libvorbis.so
%{_libdir}/libvorbisfile.a
%{_libdir}/libvorbisfile.la
%{_libdir}/libvorbisfile.so
%{_libdir}/libvorbisenc.a
%{_libdir}/libvorbisenc.la
%{_libdir}/libvorbisenc.so
%{_libdir}/pkgconfig/vorbis.pc
%{_libdir}/pkgconfig/vorbisfile.pc
%{_libdir}/pkgconfig/vorbisenc.pc

%changelog
* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of spec file.
