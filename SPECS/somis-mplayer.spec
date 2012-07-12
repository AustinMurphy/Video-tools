#SOMIS DEFS:
%define upstreamname mplayer

%define desktop_vendor  atrpms
%define snapshot snap20120311

Summary: MPlayer, the Movie Player for Linux
Name: somis-mplayer
Version: 1.0
Release: 90_%{snapshot}%{?dist}
Epoch: 4
License: GPLv2
Group: Applications/Multimedia
Source0: ftp://ftp.mplayerhq.hu/MPlayer/releases/mplayer-snapshot.tar.bz2
Source1: http://www.ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
URL: http://mplayerhq.hu/
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: somis-x264-devel
BuildRequires: somis-speex-devel >= 1.1
Provides: mencoder = %{evr}
Obsoletes: mencoder < %{evr}

%description
MPlayer is a movie player. It plays most MPEG, VOB, AVI, OGG/OGM,
VIVO, ASF/WMA/WMV, QT/MOV/MP4, FLI, RM, NuppelVideo, YUV4MPEG, FILM,
RoQ, PVA files, supported by many native, XAnim, and Win32 DLL
codecs. You can watch VideoCD, SVCD, DVD, 3ivx, DivX 3/4/5 and even
WMV movies, too (without the avifile library).

Another great feature of MPlayer is the wide range of supported output
drivers. It works with X11, XV, DGA, OpenGL, SVGAlib, fbdev, AAlib,
DirectFB, but you can use GGI, SDL (and this way all their drivers),
VESA (on every VESA compatible card, even without X11!) and some low
level card-specific drivers (for Matrox, 3Dfx and ATI), too! Most of
them support software or hardware scaling, so you can enjoy movies in
fullscreen. MPlayer supports displaying through some hardware MPEG
decoder boards, such as the Siemens DVB, DXR2 and DXR3/Hollywood+!

MPlayer has an onscreen display (OSD) for status information, nice big
antialiased shaded subtitles and visual feedback for keyboard
controls. European/ISO 8859-1,2 (Hungarian, English, Czech, etc),
Cyrillic and Korean fonts are supported along with 9 subtitle formats
(MicroDVD, SubRip, SubViewer, Sami, VPlayer, RT, SSA, AQTitle, JACOsub
and our own: MPsub). DVD subtitles (SPU streams, VobSub and Closed
Captions) are supported.

%prep
%setup -q -n %{upstreamname}-checkout-2012-06-26 -a1
# Avoid standard rpaths for xmms on lib64 archs:
sed -i -e 's,_xmmslibdir=.*/lib,_xmmslibdir=%{_libdir},g' configure
sed -i -e 's, "-lungif",,' configure
# Fix ru encoding (ATrpms bug #1516)
doconv() {
    iconv -f $1 -t $2 -o DOCS/man/$3/mplayer.1.utf8 DOCS/man/$3/mplayer.1 && \
    mv DOCS/man/$3/mplayer.1.utf8 DOCS/man/$3/mplayer.1
}
for lang in de es fr it ; do doconv iso-8859-1 utf-8 $lang ; done
for lang in hu pl ; do doconv iso-8859-2 utf-8 $lang ; done
for lang in ru ; do doconv koi8-r utf-8 $lang ; done


%build
env \
%ifarch x86_64
host_arch=x86_64 \
proc=x86_64 \
iproc=x86_64 \
%endif
./configure \
        --extra-cflags="-I%{_includedir}/directfb" \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --datadir=%{_datadir}/mplayer \
        --confdir=%{_sysconfdir}/mplayer \
        --mandir=%{_mandir} \
        --disable-liba52 \
        --disable-libdirac-lavc \
        --disable-faad \
        --disable-libopencore_amrnb \
        --disable-libopencore_amrwb \
        --disable-vdpau \
        --disable-libgsm

%if %{with directfb}
perl -pi -e"s,^DIRECTFB_INC .*,DIRECTFB_INC =`pkg-config --cflags directfb`," config.mak
perl -pi -e"s,^DIRECTFB_LIB .*,DIRECTFB_LIB =`pkg-config --libs directfb`," config.mak
%endif

make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

cat > %{buildroot}%{_sysconfdir}/mplayer/mplayer.conf << EOF
EOF

%ifarch %ix86
cp -a ./%{_sysconfdir}/codecs.conf %{buildroot}/%{_sysconfdir}/mplayer/codecs.conf
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, 755)
%doc AUTHORS Changelog DOCS/ README etc/*.conf
#%dir %{_sysconfdir}/mplayer
%ifarch %ix86
%config %{_sysconfdir}/mplayer/codecs.conf
%endif
%config %{_sysconfdir}/mplayer/mplayer.conf
%{_bindir}/*
%{_mandir}/man1/*.1*

%changelog
* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of spec file.


