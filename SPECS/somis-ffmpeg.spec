# SOMIS defs:
%define upstreamname ffmpeg
%define modname ffmpeg

### 

%define _jvmlibdir  /usr/lib/jvm
%define _jvmcommonlibdir  /usr/lib/jvm-common
%define _jnidir	          /usr/lib/java
%define _jvmcommonlibdir  /usr/lib/jvm-commmon
%define _jvmdir	    /usr/lib/jvm
%define _jvmjardir  /usr/lib/jvm-exports
%define _jvmlibdir  /usr/lib/jvm
%define _jvmprivdi  /usr/lib/jvm-private


### No package yet
%define _without_nut 1
%define _without_openjpeg 1
%define _without_vpx 1

## Use native vorbis
%define _without_vorbis 1

### Use native xvid
%define _without_xvid 1

### Disabled speex support as ffmpeg needs speex 1.2 and RHEL5 ships with 1.0.5
### Somis package somis-speex should be availible in somis repository.

%{?el5:%define _without_rtmp 1}
%{?el5:%define _without_theora 1}

%{?el4:%define _without_rtmp 1}
%{?el4:%define _without_texi2html 1}
%{?el4:%define _without_theora 1}
%{?el4:%define _without_v4l2 1}
%{?el4:%define _without_vdpau 1}

%{?el3:%define _without_rtmp 1}
%{?el3:%define _without_texi2html 1}
%{?el3:%define _without_theora 1}
%{?el3:%define _without_v4l2 1}
%{?el3:%define _without_vdpau 1}

Summary: Utilities and libraries to record, convert and stream audio and video
Name: somis-%{modname}
Version: 0.11.1
Release: 0
License: GPL
Group: Applications/Multimedia
URL: http://ffmpeg.org/

Packager: Kyle Bender

Source: http://www.ffmpeg.org/releases/ffmpeg-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Conflicts: ffmpeg

#BuildRequires: SDL-devel
BuildRequires: freetype-devel
BuildRequires: imlib2-devel
BuildRequires: zlib-devel
BuildRequires: somis-libfaac-devel
BuildRequires: somis-lame-devel
BuildRequires: somis-libogg-devel 
BuildRequires: somis-libtheora-devel
BuildRequires: somis-libogg-devel
BuildRequires: somis-libvorbis-devel
BuildRequires: somis-libvpx-devel
BuildRequires: somis-x264-devel
BuildRequires: somis-speex-devel

%description
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

Available rpmbuild rebuild options :
--without : lame vorbis theora faad faac gsm xvid x264 altivec

%package devel
Summary: Header files and static library for the ffmpeg codec library
Group: Development/Libraries
Requires: %{name} = %{version}
#Requires: imlib2-devel, SDL-devel, freetype-devel, zlib-devel, pkgconfig 
Requires: imlib2-devel, freetype-devel, zlib-devel, pkgconfig 
Requires: somis-libfaac-devel
Requires: somis-lame-devel
Requires: somis-libogg-devel
Requires: somis-libtheora-devel
Requires: somis-libogg-devel
Requires: somis-libvorbis-devel
Requires: somis-libvpx-devel
Requires: somis-x264-devel

%description devel
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

Install this package if you want to compile apps with ffmpeg support.

%package libpostproc
Summary: Video postprocessing library from ffmpeg
Group: System Environment/Libraries
Provides: ffmpeg-libpostproc-devel = %{version}-%{release}
Provides: libpostproc = 1.0-1
Provides: libpostproc-devel = 1.0-1
Obsoletes: libpostproc < 1.0-1
Obsoletes: libpostproc-devel < 1.0-1
Requires: pkgconfig

%description libpostproc
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.

This package contains only ffmpeg's libpostproc post-processing library which
other projects such as transcode may use. Install this package if you intend
to use MPlayer, transcode or other similar programs.

%prep
%setup  -q -n %{upstreamname}-%{version}

%build
export CFLAGS="%{optflags}"
# We should be using --disable-opts since configure is adding some default opts
# to ours (-O3), but as of 20061215 the build fails on asm stuff when it's set
./configure \
    --prefix="%{_prefix}" \
    --libdir="%{_libdir}" \
    --shlibdir="%{_libdir}" \
    --mandir="%{_mandir}" \
    --incdir="%{_includedir}" \
    --disable-avisynth \
    --enable-libspeex \
%{?_without_v4l:--disable-indev="v4l"} \
%{?_without_v4l2:--disable-indev="v4l2"} \
%ifarch %ix86
    --extra-cflags="%{optflags}" \
%endif
%ifarch x86_64
    --extra-cflags="%{optflags} -fPIC" \
%endif
   --enable-libfaac \
%{!?_without_lame:--enable-libmp3lame} \
%{!?_without_nut:--enable-libnut} \
    --enable-libtheora \
    --enable-libvorbis \
    --enable-libx264 \
%{!?_without_xvid:--enable-libxvid} \
    --enable-gpl \
    --enable-nonfree \
%{!?_without_openjpeg:--enable-libopenjpeg} \
    --enable-pic \
    --enable-postproc \
    --enable-libvpx \
    --enable-pthreads \
    --enable-shared \
    --enable-swscale \
%{!?_without_vdpau:--enable-vdpau} \
    --enable-version3 

%{__make} %{?_smp_mflags}
make tools/qt-faststart

%install
%{__rm} -rf %{buildroot} _docs
%{__make} install DESTDIR="%{buildroot}"
mv tools/qt-faststart %{buildroot}/usr/bin

# Remove unwanted files from the included docs
%{__cp} -a doc _docs
%{__rm} -rf _docs/{Makefile,*.texi,*.pl}

# The <postproc/postprocess.h> is now at <ffmpeg/postprocess.h>, so provide
# a compatibility symlink
%{__mkdir_p} %{buildroot}%{_includedir}/postproc/
%{__ln_s} ../ffmpeg/postprocess.h %{buildroot}%{_includedir}/postproc/postprocess.h

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig
chcon -t textrel_shlib_t %{_libdir}/libav{codec,device,format,util}.so.*.*.* &>/dev/null || :

%postun -p /sbin/ldconfig

%post libpostproc -p /sbin/ldconfig
%postun libpostproc -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc Changelog COPYING* CREDITS INSTALL MAINTAINERS README
%doc %{_mandir}/man1/ffprobe.1*
%doc %{_mandir}/man1/ffmpeg.1*
%doc %{_mandir}/man1/ffplay.1*
%doc %{_mandir}/man1/ffserver.1*
%{_bindir}/qt-faststart
%{_bindir}/ffprobe
%{_bindir}/ffmpeg
%{_bindir}/ffplay
%{_bindir}/ffserver
%{_datadir}/ffmpeg/
%{_libdir}/libavcodec.so.*
%{_libdir}/libavdevice.so.*
%{_libdir}/libavfilter.so.*
%{_libdir}/libavformat.so.*
%{_libdir}/libavutil.so.*
%{_libdir}/libswscale.so.*
%{_includedir}/postproc/
%{_libdir}/pkgconfig/libpostproc.pc
%{_libdir}/libpostproc.so*
%{_libdir}/libswresample*

#%{_libdir}/vhook/

%files devel
%defattr(-, root, root, 0755)
%doc _docs/*
%{_includedir}/libavcodec/
%{_includedir}/libavdevice/
%{_includedir}/libavfilter/
%{_includedir}/libavformat/
%{_includedir}/libavutil/
%{_includedir}/libswscale/
%{_includedir}/libswresample/swresample.h
%{_libdir}/libavcodec*
%{_libdir}/libavdevice*
%{_libdir}/libavfilter*
%{_libdir}/libavformat.a
%{_libdir}/libavutil.a
%{_libdir}/libswscale.a
%{_libdir}/libavcodec.so
%{_libdir}/libavdevice.so
%{_libdir}/libavfilter.so
%{_libdir}/libavformat.so
%{_libdir}/libavutil.so
%{_libdir}/libswscale.so
%{_libdir}/pkgconfig/libavcodec.pc
%{_libdir}/pkgconfig/libavdevice.pc
%{_libdir}/pkgconfig/libavfilter.pc
%{_libdir}/pkgconfig/libavformat.pc
%{_libdir}/pkgconfig/libavutil.pc
%{_libdir}/pkgconfig/libswscale.pc
%{_includedir}/postproc/
%{_libdir}/pkgconfig/libpostproc.pc
%{_libdir}/pkgconfig/libswresample.pc

%files libpostproc
%defattr(-, root, root, 0755)
%{_includedir}/libpostproc/
%{_includedir}/postproc/
%{_includedir}/libswresample/swresample.h
%{_libdir}/libpostproc.a
%{_libdir}/libpostproc.so*

%changelog
* Wed Jun 20 2012 Kyle Bender <kbende@med.upenn.edu>
- Added libx264 baseline and slow presets
* Tue Jun 19 2012 Kyle Bender <kbende@med.upenn.edu>
- Added qt-faststart to package
* Mon Jun 18 2012 Kyle Bender <kbende@med.upenn.edu>
- created custom somis spec
