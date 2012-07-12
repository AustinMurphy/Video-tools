%define name     somis-libspeex
%define upstreamname     speex
%define ver      1.2rc1
%define rel      1

%define _lib     /lib

Summary: An open-source, patent-free speech codec
Name: %name
Version: %ver
Release: %rel
License: BSD
Group: Application/Devel
Source: http://www.speex.org/download/%{upstreamname}-%{ver}.tar.gz
URL: http://www.speex.org/
Vendor: Speex
Packager: Kyle Bender <kbende@med.upenn.edu> 
BuildRoot: /var/tmp/%{upstreamname}-build-root
Docdir: /usr/share/doc
Conflicts: speex

%description
Speex is a patent-free audio codec designed especially for voice (unlike 
Vorbis which targets general audio) signals and providing good narrowband 
and wideband quality. This project aims to be complementary to the Vorbis
codec.

%package devel
Summary:	Speex development files
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Speex development files.

%changelog
* Thu Oct 03 2002 Jean-Marc Valin 
- Added devel package inspired from PLD spec file


%prep -q -n %{uptreamname}-%{version}
%setup

%build
export CFLAGS='-O3'
./configure --prefix=/usr --enable-shared --enable-static
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING AUTHORS ChangeLog NEWS README
%doc doc/manual.pdf
/usr/share/man/man1/speexenc.1*
/usr/share/man/man1/speexdec.1*
/usr/share/doc/speex/manual.pdf
%attr(755,root,root) %{_bindir}/speex*
%attr(755,root,root) %{_libdir}/libspeex*.so*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspeex*.la
%{_includedir}/speex/speex*.h
/usr/share/aclocal/speex.m4
%{_libdir}/pkgconfig/speex.pc
%{_libdir}/pkgconfig/speexdsp.pc
%{_libdir}/libspeex*.a

%changelog
* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of spec file.

