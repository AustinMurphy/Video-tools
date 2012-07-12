%define _lib    /lib
Name:		vorbis-tools
Version:	1.3.0
Release:	1
Summary:	Several Ogg Vorbis Tools

Group:		Applications/Multimedia
License:	GPL
URL:		http://xiph.org/
Vendor:		Xiph.Org Foundation <team@xiph.org>
Source:         http://downloads.xiph.org/releases/vorbis/%{name}-%{version}.tar.gz
Prefix:		%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-root

Requires:       somis-libvorbis >= 1.1.1
BuildRequires:	somis-libvorbis-devel >= 1.1.1
Requires:       flac >= 1.1.2
BuildRequires:	flac-devel >= 1.1.2
Requires:       somis-libspeex >= 1.0.2
BuildRequires:	somis-libspeex-devel >= 1.0.2
Requires:       libao >= 0.8.4
BuildRequires:	libao-devel >= 0.8.4
Requires:       curl >= 7.8
BuildRequires:	curl-devel >= 7.8

%description
vorbis-tools contains oggenc (an encoder) and ogg123 (a playback tool).
It also has vorbiscomment (to add comments to Vorbis files), ogginfo (to
give all useful information about an Ogg file, including streams in it),
oggdec (a simple command line decoder), and vcut (which allows you to 
cut up Vorbis files).

%prep
%setup -q -n %{name}-%{version}
./autogen.sh

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} --mandir=%{_mandir}
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean 
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING
%doc README
%doc ogg123/ogg123rc-example
%{_bindir}/oggenc
%{_bindir}/oggdec
%{_bindir}/ogg123
%{_bindir}/ogginfo
%{_bindir}/vorbiscomment
%{_bindir}/vcut
%{_datadir}/locale/*/LC_MESSAGES/*
%{_mandir}/man1/ogg123.1*
%{_mandir}/man1/oggenc.1*
%{_mandir}/man1/oggdec.1*
%{_mandir}/man1/ogginfo.1*
%{_mandir}/man1/vorbiscomment.1*
%{_mandir}/man1/vcut.1*

%changelog
* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of spec file.
