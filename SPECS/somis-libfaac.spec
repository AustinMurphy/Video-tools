#SOMIS DEFS
%define upstreamname faac

Summary: Reference encoder and encoding library for MPEG2/4 AAC
Name: somis-libfaac
Version: 1.28
Release: 1%{?dist}
License: LGPL
Group: Applications/Multimedia
URL: http://www.audiocoding.com/

Source: http://dl.sf.net/faac/faac-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

#BuildRequires: libmp4v2-devel
BuildRequires: autoconf >= 2.50, automake, libtool, dos2unix, gcc-c++

%description
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

%package devel
Summary: Development libraries of the FAAC AAC encoder
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

This package contains development files and documentation for libfaac.

%prep
%setup -q -n %{upstreamname}-%{version}

%build
sh bootstrap
%configure --disable-static \
    --with-mp4v2
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README TODO docs/*
%{_bindir}/faac
%{_libdir}/libfaac.so.*
%doc %{_mandir}/man1/faac.1.gz

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/faac.h
%{_includedir}/faaccfg.h
%{_libdir}/libfaac.so
%exclude %{_libdir}/libfaac.la

%changelog
* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of faac spec file.
