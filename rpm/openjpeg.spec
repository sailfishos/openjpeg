Name:    openjpeg
Version: 2.5.3
Release: 1
Summary: JPEG 2000 codec library
License:   BSD
URL:       https://github.com/sailfishos/openjpeg
BuildRequires: cmake

Source0: %{name}-%{version}.tar.bz2

%description
OpenJPEG is an open-source JPEG 2000 codec written in C language. It has been
developed in order to promote the use of JPEG 2000, the new still-image
compression standard from the Joint Photographic Experts Group (JPEG).

%package utils
Summary: OpenJPEG command-line tools
Requires: openjpeg = %{version}-%{release}

%description utils
The openjpeg-utils package contains command-line tools.

%package  devel
Summary:  Development files for openjpeg
Requires: openjpeg = %{version}-%{release}
Requires: openjpeg-utils = %{version}-%{release}

%description devel
The openjpeg-devel package contains libraries and header files for
developing applications that use OpenJPEG.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%cmake -DBUILD_STATIC_LIBS=OFF -DBUILD_SHARED_LIBS=ON \
       -DCMAKE_BUILD_TYPE=Release \
       -DOPENJPEG_INSTALL_LIB_DIR=%{_lib}
%cmake_build

%install
%cmake_install

%check
# mostly pointless without test images, but it's a start -- Rex
# make test -C build

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/libopenjp2.so.*

%files utils
%{_bindir}/opj_compress
%{_bindir}/opj_decompress
%{_bindir}/opj_dump

%files devel
%{_includedir}/openjpeg-*/
%{_libdir}/pkgconfig
%{_libdir}/libopenjp2.so
%{_libdir}/cmake/openjpeg-*/
