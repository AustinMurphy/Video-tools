%define   upstreamname ffmpeg2theora

Name:         somis-ffmpeg2theora
License:      GNU General Public License (GPL)
Group:        Productivity/Multimedia/Other
Version:      0.28
Release:      1
Summary:      A simple converter to create Ogg Theora files
URL:          http://v2v.cc/~j/ffmpeg2theora/index.html
Source0:      http://v2v.cc/~j/ffmpeg2theora/%{upstreamname}-%{version}.tar.gz
Patch0:       ffmpeg2theora-fix-include-path.patch
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

BuildRequires: somis-ffmpeg-devel
BuildRequires: somis-libtheora-devel 
BuildRequires: somis-lame-devel
BuildRequires: somis-libkate
BuildRequires: somis-libkate-devel
BuildRequires: scons
Conflicts: ffmpeg2theora

%description
A simple converter to create Ogg Theora files.

%prep
%setup -q -n %{upstreamname}-%{version}
%patch0 -p1
PKG_CONFIG_PATH=/usr/lib64/pkgconfig:/usr/lib/pkgconfig:/usr/local/pkgconfig
export PKG_CONFIG_PATH

%build
scons prefix=%{_prefix} APPEND_CCFLAGS="%{optflags}"

%install
scons install prefix=%{_prefix} mandir=%{_mandir} destdir=%{buildroot} install
%__install -D -m 0644 ffmpeg2theora.1 %{buildroot}%{_mandir}/man1/ffmpeg2theora.1

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog COPYING AUTHORS README
%{_bindir}/ffmpeg2theora
%doc %{_mandir}/man1/ffmpeg2theora.1*

%changelog
