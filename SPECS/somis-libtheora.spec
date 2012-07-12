# SOMIS defs:
%define upstreamname libtheora

Name:		somis-libtheora
Version:	1.1.1
Release:	0..0.4.alpha5
Summary:	The Theora Video Compression Codec.

Group:		System Environment/Libraries
License:	BSD
URL:		http://www.theora.org/
Vendor:		Xiph.org Foundation <team@.org>
Source:		http://downloads..org/releases/theora/%{upstreamname}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{upstreamname}-%{version}-root

BuildRequires:	somis-libogg-devel >= 2:1.1
BuildRequires:	somis-libvorbis-devel >= 1.3.3
#BuildRequires:	SDL-devel
Conflicts: libtheora

# this needs to be explicit since vorbis's .so versioning didn't get bumped
# when going from 1.0 to 1.0.1
Requires:       somis-libvorbis >= 1.3.3

%description
Theora is Xiph.Org's first publicly released video codec, intended
for use within the Ogg's project's Ogg multimedia streaming system.
Theora is derived directly from On2's VP3 codec; Currently the two are
nearly identical, varying only in encapsulating decoder tables in the
bitstream headers, but Theora will make use of this extra freedom
in the future to improve over what is possible with VP3.

%package devel
Summary:        Development tools for Theora applications.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
#BuildRequires:  somis-libtheora >= 1.1.1
Requires:       somis-libogg-devel >= 2:1.1

%description devel
The libtheora-devel package contains the header files and documentation
needed to develop applications with Ogg Theora.

%prep
%setup -q -n %{upstreamname}-%{version}

%build
%configure --enable-shared
make

%install
rm -rf $RPM_BUILD_ROOT
# make sure our temp doc build dir is removed
rm -rf $(pwd)/__docs

%makeinstall docdir=$(pwd)/__docs

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean 
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING README
%{_libdir}/libtheora.so.*
%{_libdir}/libtheoradec.so.1
%{_libdir}/libtheoraenc.so.1
%{_libdir}/libtheoradec.a
%{_libdir}/libtheoradec.a
%{_libdir}/libtheoradec.so
%{_libdir}/libtheoradec.so.1.1.4
%{_libdir}/libtheoraenc.a
%{_libdir}/libtheoraenc.so
%{_libdir}/libtheoraenc.so.1.1.2

%files devel
%defattr(-,root,root,-)
%doc __docs/*
%{_libdir}/libtheora.a
%{_libdir}/libtheora.so
%dir %{_includedir}/theora
%{_includedir}/theora/codec.h
%{_includedir}/theora/theora.h
%{_includedir}/theora/theoraenc.h
%{_includedir}/theora/theoradec.h
%{_libdir}/pkgconfig/theora.pc
%{_libdir}/pkgconfig/theoradec.pc
%{_libdir}/pkgconfig/theoraenc.pc


%changelog
* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of spec file.

