#SOMIS DEFS:
%define upstreamname t1lib

Summary: PostScript Type 1 font rasterizer
Name:    somis-t1lib
Version: 5.1.2
Release: 1%{?dist}
License: LGPL
Group:   Applications/Publishing
URL:     http://www.t1lib.org/

Source:    http://ibiblio.org/pub/Linux/libs/graphics/t1lib-%{version}.tar.gz
Patch1:    t1lib-5.0.0-xglyph-env.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Conflicts: t1lib

%description
T1lib is a rasterizer library for Adobe Type 1 Fonts. It supports
rotation and transformation, kerning underlining and antialiasing. It
does not depend on X11, but does provides some special functions for
X11.

AFM-files can be generated from Type 1 font files and font subsetting
is possible.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup  -q -n %{upstreamname}-%{version}
%patch1 -p1

%build
%configure  --without-x 

%{__make} %{?_smp_mflags}
%{__ln_s} README.t1lib-%{version} README

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%{__rm} -rf %{buildroot}%{_datadir}/t1lib/

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig
%{_sbindir}/t1libconfig --force &>/dev/null || :

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc Changes LGPL LICENSE README
%{_bindir}/type1afm
%{_libdir}/libt1.so.*

%files devel
%defattr(-, root, root, 0755)
%doc doc/t1lib_doc.pdf
%{_includedir}/t1lib.h
%{_libdir}/libt1.a
%exclude %{_libdir}/libt1.la
%{_libdir}/libt1.so

%changelog
* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of spec file.

