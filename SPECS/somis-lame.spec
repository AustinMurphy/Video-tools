%define name somis-lame
%define ver 3.99.5
%define rel 1
%define prefix %{_usr}
%define docdir %{_defaultdocdir}

%define upstreamname lame 

Summary : LAME Ain't an MP3 Encoder... but it's the best.
Summary(fr) : LAME n'est pas un encodeur MP3 ;->
Name: %{name}
Version: %{ver}
Release: %{rel}
License: LGPL
Vendor: The LAME Project
Packager: Kyle Bender <kbende@med.upenn.edu>
URL: http://www.mp3dev.org
Group: Applications/Multimedia
Source: %{upstreamname}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-root
Requires: ncurses >= 5.0
BuildRequires: gcc => 3.0.1, /usr/bin/find, ncurses-devel
%ifarch %{ix86} x86_64
BuildRequires: nasm
%endif
Conflicts: lame
Provides: mp3encoder

%description
LAME is an educational tool to be used for learning about MP3 encoding.  The
goal of the LAME project is to use the open source model to improve the
psycho acoustics, noise shaping and speed of MP3. 

%description -l fr
LAME est un outil d'enseignement pour l'apprentissage de l'encodage MP3.
Le but du projet LAME est d'utiliser un mod�le "open source" afin
d'am�liorer la qualit� et la vitesse du MP3. 



%package devel
Summary: Shared and static libraries for LAME.
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
LAME is an educational tool to be used for learning about MP3 encoding.
This package contains both the shared and the static libraries from the
LAME project.

You will also need to install the main lame package in order to install
these libraries.

%prep
%setup -q -n %{upstreamname}-%{version}

%build

# Vorbis makes the build fail for now. . .
rm -f config.cache
 
%configure \
%ifarch %{ix86} x86_64
	--enable-nasm \
%endif
	--enable-decoder \
	--without-vorbis \
	--enable-analyzer=no \
	--enable-brhist \
	--disable-debug
%{__make} %{?_smp_mflags} test CFLAGS="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%makeinstall

### Some apps still expect to find <lame.h>
%{__ln_s} -f lame/lame.h %{buildroot}%{_includedir}/lame.h


find doc/html -name "Makefile*" | xargs rm -f
### make install really shouldn't install these
%{__rm} -rf %{buildroot}%{_docdir}/lame/


%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null

%clean
%{__rm} -rf %{buildroot}

%files
%defattr (-,root,root)
%doc COPYING ChangeLog README TODO USAGE doc/html
%doc doc/html
%{_bindir}/lame
%{_libdir}/libmp3lame.so.*
%{_mandir}/man1/lame.1*

%files devel
%defattr (-, root, root)
%doc API HACKING STYLEGUIDE
%{_libdir}/libmp3lame.a
%{_libdir}/libmp3lame.la
%{_libdir}/libmp3lame.so
%{_includedir}/*

%changelog

* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of lame spec file.
