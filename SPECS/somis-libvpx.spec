# SOMIS defs:
%define upstreamname libvpx
%define _libdir  /usr/lib

%define major 0
%define libname %mklibname vpx %major
%define develname %mklibname -d vpx

Name:			somis-libvpx
Summary:		VP8 Video Codec SDK
Version:		1.1.0
Release:		1
License:		BSD
Group:			System/Libraries
Source0:		http://webm.googlecode.com/files/%{upstreamname}-1.1.0.tar.gz
URL:			http://www.webmproject.org/tools/vp8-sdk/
Packager:               Kyle Bender <kbende@med.upenn.edu>
BuildRoot:              /var/tmp/%{name}-%{version}-%{release}
Conflicts:              libvpx

%description
libvpx provides the VP8 SDK, which allows you to integrate your applications 
with the VP8 video codec, a high quality, royalty free, open source codec 
deployed on millions of computers and devices worldwide. 

%package devel
Summary:        libvpx devel
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
libvpx provides the VP8 SDK, which allows you to integrate your applications
with the VP8 video codec, a high quality, royalty free, open source codec
deployed on millions of computers and devices worldwide.


%prep
%setup -q -n %{upstreamname}-%{version}

# fix permissions
chmod 644 AUTHORS CHANGELOG LICENSE README

%build

./configure --enable-shared --enable-pic --disable-install-docs

make 


%install
#export INSTALL_ROOT="$RPM_BUILD_ROOT"
make DIST_DIR=$RPM_BUILD_ROOT%{_prefix} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)

#%dir %{prefix}

%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG LICENSE README
%{_libdir}/libvpx.a
%{_libdir}/libvpx.so
%{_libdir}/libvpx.so.1
%{_libdir}/libvpx.so.1.1
%{_libdir}/libvpx.so.1.1.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/vpx/
%{_bindir}/*

%changelog
* Thu May 31 2012 Kyle Bender<kbende@med.upenn.edu>
- Create somis verion of spec file.
