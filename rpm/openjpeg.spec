Name:    openjpeg
Version: 2.3.0
Release: 1
Summary: JPEG 2000 codec library

Group:     System/Libraries
License:   BSD
URL:       http://www.openjpeg.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake
BuildRequires: libtiff-devel

Source0: https://github.com/uclouvain/%{name}/archive/%{name}-%{version}.tar.gz

Patch5: openjpeg-svn480-use-stdbool.patch
Patch21: openjpeg-20070717svn-mqc-optimize.patch

%description
OpenJPEG is an open-source JPEG 2000 codec written in C language. It has been
developed in order to promote the use of JPEG 2000, the new still-image
compression standard from the Joint Photographic Experts Group (JPEG).

%package utils
Summary: OpenJPEG command-line tools
Group:   Applications/Multimedia
Requires: openjpeg = %{version}-%{release}

%description utils
The openjpeg-utils package contains command-line tools.

%package  devel
Summary:  Development files for openjpeg
Group:    Development/Libraries
Requires: openjpeg = %{version}-%{release}

%description devel
The openjpeg-devel package contains libraries and header files for
developing applications that use OpenJPEG.

%prep
%setup -q -n %{name}-%{version}/upstream
%patch5 -p1
%patch21 -p1

%build
if [ ! -d build ] ; then mkdir build; fi
pushd build
%cmake .. -DBUILD_EXAMPLES:BOOL=ON
make %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}
pushd build
make install DESTDIR="%{buildroot}"
rm %{buildroot}%{_libdir}/libopenjp2.a
popd

%check
# mostly pointless without test images, but it's a start -- Rex
# make test -C build

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/libopenjp2.so.*

%files utils
%defattr(-,root,root,-)
%{_bindir}/opj_compress
%{_bindir}/opj_decompress
%{_bindir}/opj_dump

%files devel
%defattr(-,root,root,-)
%{_includedir}/openjpeg-2.3/
%{_libdir}/pkgconfig
%{_libdir}/libopenjp2.so
%{_libdir}/openjpeg-2.3/

