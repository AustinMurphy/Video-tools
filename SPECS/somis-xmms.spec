%define	name	somis-xmms
%define	upstreamname	xmms
%define	version	1.2.11
%define	release	1
%define	epoch	1
%define	prefix	/usr

## Check to see if libGL is installed. Build xmms-gl if it is.
%define withGL	%(if [ -z "`rpm -q --whatprovides libGL.so.1 2>/dev/null | grep -v '^no package provides'`" ]; then echo 0; else echo 1; fi)

## Check to see if libmikmod is installed. Build xmms-mikmod if it is.
%define withmm	%(if [ -z "`rpm -q --whatprovides libmikmod.so.2 2>/dev/null | grep -v '^no package provides'`" ]; then echo 0; else echo 1; fi)
%define wmmdev	%(if [ -z "`rpm -q --whatprovides $(/usr/bin/which libmikmod-config 2>/dev/null) 2>/dev/null | grep -v '^no package provides'`" ]; then echo 0; else echo 1; fi)

## Check to see if libvorbisfile is installed.  Build xmms-vorbis if it is.
%define withvorbis %(if [ -z "`rpm -q --whatprovides libvorbisfile.so.3 2>/dev/null | grep -v '^no package provides'`" ]; then echo 0; else echo 1; fi)

## Check to see if libalsa is installed.  Build xmms-alsa if it is.
%define withalsa %(if [ -z "`rpm -q --whatprovides libasound.so.2 2>/dev/null | grep -v '^no package provides'`" ]; then echo 0; else echo 1; fi)

## Check to see if libesd is installed.  Build xmms-esd if it is.
%define withesd %(if [ -z "`rpm -q --whatprovides /usr/bin/esd-config 2>/dev/null | grep -v '^no package provides'`" ]; then echo 0; else echo 1; fi)

## Funky hack to get package names that provide libmikmod and libmikmod-config
## Becuase of the differing package names between redhat, mandrake, etc.
%if %{withmm} == 1
%define mikmod	%(rpm -q --qf '%{NAME}' --whatprovides libmikmod.so.2)
%endif
%if %{withmm} && %{wmmdev}
%define mmdev   %(rpm -q --qf '%{NAME}' --whatprovides $(/usr/bin/which libmikmod-config))
%endif
%if %{withmm} && ! %{wmmdev}
%define mmdev   /usr/bin/libmikmod-config
%endif

Summary:	XMMS - Multimedia player for the X Window System.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Applications/Multimedia
Vendor:		XMMS Development Team <bugs@xmms.org>
Url:		http://www.xmms.org/
Source:		%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Obsoletes:	x11amp, x11amp0.7-1-1, xmms-mpg123, xmms-mp3
Requires:	gtk+ >= 1:1.2.2
BuildPrereq:	gtk+-devel
Conflicts:	xmms

%description
X MultiMedia System is a sound player written from scratch. Since it 
uses the WinAmp GUI, it can use WinAmp skins. It can play mp3s, mods, s3ms,
and other formats. It now has support for input, output, general, and
visualization plugins.

%package	devel
Summary:	XMMS - Static libraries and header files.
Group:		Applications/Multimedia
Obsoletes:	x11amp-devel
Requires:	%{name} = %{epoch}:%{version}, glib-devel >= 1:1.2.2, gtk+-devel >= 1:1.2.2

%description	devel
Static libraries and header files required for compiling xmms plugins.

%if %{withesd} == 1
%package	esd
Summary:	XMMS - Output plugin for use with the esound package.
Group:		Applications/Multimedia
Requires:	%{name} >= %{epoch}:%{version}
Obsoletes:	x11amp-esd
Requires:	esound >= 0.2.8

%description	esd
Output plugin for xmms for use with the esound package
%endif

%if %{withmm} == 1
%package	mikmod
Summary:	XMMS - Input plugin to play MODs.
Group:		Applications/Multimedia
Obsoletes:	x11amp-mikmod
Requires:	%{name} >= %{epoch}:%{version}
Requires:	%{mikmod} >= 3.1.6
BuildPrereq:	%{mmdev}

%description	mikmod
Input plugin for XMMS to play MODs (.MOD,.XM,.S3M, etc)
%endif

%if %{withvorbis} == 1
%package	vorbis
Summary:	XMMS - Input plugin to play OGGs
Group:		Applications/Multimedia
Requires:	%{name} >= %{epoch}:%{version}
Requires:	somis-libogg >= 1.0
Requires:	somis-libvorbis >= 1.0
BuildPrereq:	somis-libogg-devel
BuildPrereq:	somis-libvorbis-devel

%description	vorbis
Input plugin for XMMS to play Ogg Vorbis files (.ogg).
%endif

%if %{withGL} == 1
%package 	gl
Summary:	XMMS - Visualization plugins that use the Mesa3d library.
Group:		Applications/Multimedia
Requires:	%{name} = %{epoch}:%{version}
Obsoletes:	xmms-mesa

%description	gl
Visualization plugins that use the Mesa3d library.
%endif

%if %{withalsa} == 1
%package	alsa
Summary:	XMMS - ALSA output plugin
Group:		Applications/Multimedia
Requires:	%{name} >= %{epoch}:%{version}
Requires:	alsa-lib >= 0.9.0

%description	alsa
Output plugin for XMMS to use with the Advanced Linux Sound
Architecture (ALSA).
%endif

%prep
%setup -q -n %{upstreamname}-%{version}

%build
unset LINGUAS || :;

%configure
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && [ -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT};
mkdir -p ${RPM_BUILD_ROOT}
make install DESTDIR=$RPM_BUILD_ROOT

# Install icons.
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/mini
install -m 644 xmms/xmms_logo.xpm \
	${RPM_BUILD_ROOT}%{_datadir}/pixmaps/xmms_logo.xpm
install -m 644 xmms/xmms_mini.xpm \
	${RPM_BUILD_ROOT}%{_datadir}/pixmaps/mini/xmms_mini.xpm

# Install wmconfig file
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/X11/wmconfig
install -m 644 xmms/xmms.wmconfig \
	${RPM_BUILD_ROOT}%{_sysconfdir}/X11/wmconfig/xmms

# Install applnk file
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/X11/applnk/Multimedia/                             
install -m 644 xmms/xmms.desktop \
	${RPM_BUILD_ROOT}%{_sysconfdir}/X11/applnk/Multimedia/ 

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && [ -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT};

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README
%{_sysconfdir}/X11/wmconfig/xmms
%{_sysconfdir}/X11/applnk/Multimedia/xmms.desktop
%{_bindir}/xmms
%{_bindir}/wmxmms
%{_libdir}/libxmms.*
%{_libdir}/xmms/Input/libcdaudio*
%{_libdir}/xmms/Input/libmpg123*
%{_libdir}/xmms/Input/libtonegen*
%{_libdir}/xmms/Input/libwav*
%{_libdir}/xmms/Input/libvorbis*
%{_libdir}/xmms/Output/libOSS*
%{_libdir}/xmms/Output/libdisk_writer*
%{_libdir}/xmms/General/*
%{_libdir}/xmms/Effect/*
%{_libdir}/xmms/Visualization/libbscope*
%{_libdir}/xmms/Visualization/libsanalyzer*
%{_mandir}/man1/xmms.*
%{_mandir}/man1/wmxmms.*
%{_datadir}/xmms/*
%{_datadir}/locale/*/LC_MESSAGES/xmms.mo
%{_datadir}/pixmaps/xmms_logo.xpm
%{_datadir}/pixmaps/mini/xmms_mini.xpm

%files devel
%defattr(-, root, root)
%{_bindir}/xmms-config
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_includedir}/*
%{_datadir}/aclocal/xmms.m4

%if %{withesd} == 1
%files esd
%defattr(-, root, root)
%{_libdir}/xmms/Output/libesdout*
%endif

%if %{withmm} == 1
%files mikmod
%defattr(-, root, root)
%{_libdir}/xmms/Input/libmikmod*
%endif

%if %{withvorbis} == 1
%files vorbis
%defattr(-, root, root)
%{_libdir}/xmms/Input/libvorbis*
%endif

%if %{withGL} == 1
%files gl
%defattr(-, root, root)
%{_libdir}/xmms/Visualization/libogl_spectrum*
%endif

%if %{withalsa} == 1
%files alsa
%defattr(-, root, root)
%{_libdir}/xmms/Output/libALSA*
%endif

%changelog
* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of spec file.


