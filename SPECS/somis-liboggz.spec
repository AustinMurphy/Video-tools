#SOMIS DEFS
%define _prefix  /usr
%define _lib    lib
%define upstreamname liboggz

Name:          somis-liboggz
Version:       1.0.2
Release:       0
Summary:       Simple programming interface for Ogg files and streams
Group:         System/Libraries
Vendor:        somis
Distribution:  somis
Packager:      Kyle Bender <kbende@med.upenn.edu>
URL:           http://www.xiph.org/oggz/
Source:        http://downloads.xiph.org/releases/liboggz/liboggz-%{version}.tar.gz
License:       BSD
Requires:      somis-libogg
#Requires:      doxygen
## AUTOBUILDREQ-BEGIN
#BuildRequires: doxygen
BuildRequires: glibc-devel
BuildRequires: somis-libogg-devel
## AUTOBUILDREQ-END
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
%{name} provides a simple programming interface for reading and writing Ogg files
and streams. Ogg is an interleaving data container developed by Monty at
Xiph.Org, originally to support the Ogg Vorbis audio format.

%package devel
Group:         Development/Libraries
Summary:       Libraries and headers for %{name}
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description devel
%{name} provides a simple programming interface for reading and writing Ogg files
and streams. Ogg is an interleaving data container developed by Monty at
Xiph.Org, originally to support the Ogg Vorbis audio format.

This package contains libraries and header files need for development.

%package static
Group:         Development/Libraries
Summary:       Static libraries for %{name}
Requires:      %{name}-devel = %{?epoch:%epoch:}%{version}-%{release}

%description static
%{name} provides a simple programming interface for reading and writing Ogg files
and streams. Ogg is an interleaving data container developed by Monty at
Xiph.Org, originally to support the Ogg Vorbis audio format.

This package contains static libraries need for development.

%package tools 
Summary:       Various tools using the %{name} library
Group:         Development/Tools
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description tools
%{name} provides a simple programming interface for reading and writing Ogg files
and streams. Ogg is an interleaving data container developed by Monty at
Xiph.Org, originally to support the Ogg Vorbis audio format.

This package contains various tools using the liboggz library.

%package doc
Group:         Documentation
Summary:       Documentation for %{name}
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description doc
%{name} provides a simple programming interface for reading and writing Ogg files
and streams. Ogg is an interleaving data container developed by Monty at
Xiph.Org, originally to support the Ogg Vorbis audio format.

This package contains HTML documentation need for development.

%prep
%setup -q -n %{upstreamname}-%{version}

%build
./configure  --prefix=/usr --enable-shared
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
make clean 

%files
%defattr(-,root,root)
%{_libdir}/liboggz.so.*
%doc AUTHORS COPYING ChangeLog README 

%files devel
%defattr(-,root,root)
%dir %{_includedir}/oggz
%{_includedir}/oggz/oggz*.h
%{_libdir}/liboggz.so
%{_exec_prefix}/lib/pkgconfig/oggz.pc

%files static
%defattr(-,root,root)
%{_libdir}/liboggz.*a

%files tools
%defattr(-,root,root)
%{_bindir}/oggz*
%{_mandir}/man1/oggz*.1.gz

%files doc
%defattr(-,root,root)
%doc %{_docdir}/liboggz/html
%doc %{_docdir}/liboggz/latex

%changelog
* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of spec file.
