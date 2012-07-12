
%define name	somis-normalize
%define upstreamname	normalize
%define version	0.7.7
%define release	1

%ifos Linux
    %define _prefix /usr
%else
    %define _prefix /usr/local
%endif
%define uown root
%define gown root

%define installexec %{_bindir}/install

Prefix: %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Summary: A tool for adjusting the volume of audio files to a standard level.
Name:    %{name}
Version: %{version}
Release: %{release}
License:: GPL
%if %(rpm -q redhat-release > /dev/null 2>&1 && echo 1 || echo 0)
%define	mygroup Applications/Sound
%endif
%if %(rpm -q mandrake-release > /dev/null 2>&1 && echo 1 || echo 0)
%define	mygroup Applications/Multimedia
%else
%define	mygroup Applications/Multimedia
%endif
Group: %{mygroup}
Source: http://savannah.nongnu.org/download/%{upstreamname}/%{upstreamname}-%{version}.tar.bz2

%description
normalize is a tool for adjusting the volume of audio files to a
standard level.  This is useful for things like creating mixed CD's
and mp3 collections, where different recording levels on different
albums can cause the volume to vary greatly from song to song.

%package        xmms
Summary:        Normalize - XMMS plugin to apply volume adjustments
Group:		%{mygroup}
Requires:       %{upstreamname} = %{version}, gtk+ >= 1.2.2, xmms >= 1.0.0
BuildPrereq:    gtk+-devel >= 1.2.2, xmms-devel
Conflicts:      normalize

%description    xmms
Plugin for XMMS to honor volume adjustments (RVA2 frames) in ID3 tags

%prep
%setup -q -n %{upstreamname}-%{version}
autoconf configure.ac

%build
./configure \
    --disable-helper-search \
    --enable-xmms \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --prefix=%{_prefix} \
    --without-audiofile

make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
[ "%{buildroot}" != "/" ] && [ -d %{buildroot} ] && rm -rf %{buildroot};
mkdir -p $RPM_BUILD_ROOT
strip -x xmms-rva/.libs/librva.so
make install-strip DESTDIR=$RPM_BUILD_ROOT

find %{buildroot} \! -type d -print \
    | sed "s@^%{buildroot}@@g" \
    > %{name}-%{version}-filelist

%clean
[ "%{buildroot}" != "/" ] && [ -d %{buildroot} ] && rm -rf %{buildroot};

%files
%defattr(-,%{uown},%{gown},-)
%doc README COPYING
%{_bindir}/normalize
%{_bindir}/normalize-mp3
%{_bindir}/normalize-ogg
%{_mandir}/man1/normalize.1*
%{_mandir}/man1/normalize-mp3.1*
%{_datadir}/locale/en_GB/LC_MESSAGES/normalize.mo
%{_datadir}/locale/fr/LC_MESSAGES/normalize.mo

%files xmms
%defattr(-,%{uown},%{gown},-)
/usr/lib64/xmms/Effect/librva.la
/usr/lib64/xmms/Effect/librva.so

%changelog
* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of spec file.

