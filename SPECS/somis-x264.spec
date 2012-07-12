# SOMIS defs:
%define upstreamname x264
%define name x264

### libquicktime fails to build with this on EL3
# ExcludeDist: el2 el3
%{?el4:%define _without_modxorg 1}

%{?el3:%define _without_asm 1}
%{?el3:%define _without_glibc232 1}
%{?el3:%define _without_modxorg 1}

%define date 20120523

Summary: Library for encoding and decoding H264/AVC video streams
Name: somis-%{name}
Version: 0.0.0
Release: 0.4.%{date}%{?dist}
License: GPL
Group: System Environment/Libraries
URL: http://developers.videolan.org/x264.html

Source: http://downloads.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-%{date}-2245.tar.bz2
Patch0: x264-20090708-glibc232.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gettext
BuildRequires: nasm
BuildRequires: yasm
Conflicts: x264
%{?_with_visualize:%{!?_without_modxorg:BuildRequires: libXt-devel}}
%{?_with_visualize:%{?_without_modxorg:BuildRequires: XFree86-devel}}

Obsoletes: x264-gtk <= %{version}-%{release}

%description
Utility and library for encoding H264/AVC video streams.

%package devel
Summary: Development files for the x264 library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, pkgconfig
Obsoletes: x264-gtk-devel <= %{version}-%{release}

%description devel
This package contains the files required to develop programs that will encode
H264/AVC video streams using the x264 library.

%prep
%setup -n %{upstreamname}-snapshot-%{date}-2245
# configure hardcodes X11 lib path
%{__perl} -pi -e 's|/usr/X11R6/lib |/usr/X11R6/%{_lib} |g' configure

### Required for glibc < 2.3.2 (http://article.gmane.org/gmane.comp.video.x264.devel/1696)
%{?_without_glibc232:%patch0 -p0}

%build
# Force PIC as applications fail to recompile against the lib on x86_64 without
./configure \
    --prefix="%{_prefix}" \
    --bindir="%{_bindir}" \
    --includedir="%{_includedir}" \
    --libdir="%{_libdir}" \
    --enable-debug \
    --enable-pic \
    --enable-pthread \
    --enable-shared \
%{?_with_visualize:--enable-visualize} \
    --extra-cflags="%{optflags}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING
%{_bindir}/x264
%{_libdir}/libx264.so.*
%{_includedir}/x264_config.h

%files devel
%defattr(-, root, root, 0755)
%doc doc/*.txt
%{_includedir}/x264.h
%{_libdir}/pkgconfig/x264.pc
#%{_libdir}/libx264.a
%{_libdir}/libx264.so

%changelog
* Thu Jun 07 2012 Kyle Bender <kbende@med.upenn.edu> 
- Created SPEC for x264
