# reset patch fuzz, rebasing patches will require delicate surgery -- Rex
%define _default_patch_fuzz 2

Name:    openjpeg
Version: 1.3
Release: 6
Summary: OpenJPEG command line tools

Group:     Applications/Multimedia
License:   BSD
URL:       http://www.openjpeg.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake
BuildRequires: libtiff-devel

Source0: http://www.openjpeg.org/OpenJPEG_v1_3.tar.gz

Patch1: openjpeg-20070717svn-codec-libtiff.patch
Patch4: openjpeg-svn480-cmake.patch
Patch5: openjpeg-svn480-use-stdbool.patch
Patch6: openjpeg-1.3-tcd_init_encode-alloc-fix.patch
Patch7: openjpeg-1.3-reverse-bogus-aligned-malloc.patch
Patch44: openjpeg-svn468-mj2-noscroll.patch
Patch21: openjpeg-20070717svn-mqc-optimize.patch
Patch22: openjpeg-20070821svn-t1-remove-macro.patch
Patch23: openjpeg-20070719svn-t1-x86_64-flags-branchless.patch
Patch24: openjpeg-20070719svn-t1-t1_dec_sigpass_step-optimize.patch
Patch25: openjpeg-20070821svn-t1-flags-stride.patch
Patch26: openjpeg-20070821svn-t1-updateflags-x86_64.patch
Patch27: openjpeg-svn470-t1-flags-mmx.patch
Patch28: openjpeg-20070719svn-mqc-more-optimize.patch
## upstreamable patches
# libopenjpeg has undefined references, http://bugzilla.redhat.com/467661
Patch51: openjpeg-1.3-fix-type-error.patch

%description
OpenJPEG is an open-source JPEG 2000 codec written in C language. It has been
developed in order to promote the use of JPEG 2000, the new still-image
compression standard from the Joint Photographic Experts Group (JPEG).

%package libs
Summary: JPEG 2000 codec library
Group:   System/Libraries

%description libs
The openjpeg-libs package contains runtime libraries for applications that use
OpenJPEG.

%package  devel
Summary:  Development files for openjpeg
Group:    Development/Libraries
Requires: openjpeg-libs = %{version}-%{release}

%description devel
The openjpeg-devel package contains libraries and header files for
developing applications that use OpenJPEG.

%prep
%setup -q -n OpenJPEG_v1_3
# Windows stuff, delete it, it slows down patch making
rm -rf jp3d
# Make sure we use system libraries
rm -rf libs
%patch1 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch44 -p1
%patch22 -p1
%patch23 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch24 -p1
%patch21 -p1
%patch28 -p1
#%patch50 -p1 -b .libm
%patch51 -p1 -b .fix-type-error

%build
mkdir build
pushd build
%cmake .. -DBUILD_EXAMPLES:BOOL=ON
make %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}
pushd build
make install DESTDIR="%{buildroot}"
popd

# HACK: until pkg-config support lands, temporarily provide
# openjpeg.h header in legacy location
ln -s openjpeg/openjpeg.h %{buildroot}%{_includedir}/openjpeg.h



chmod 644 license.txt

%check
# mostly pointless without test images, but it's a start -- Rex
make test -C build

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc license.txt
%{_bindir}/extract_j2k_from_mj2
%{_bindir}/frames_to_mj2
%{_bindir}/image_to_j2k
%{_bindir}/j2k_to_image
%{_bindir}/mj2_to_frames
%{_bindir}/wrap_j2k_in_mj2

%files libs
%defattr(-,root,root,-)
%{_libdir}/libopenjpeg.so.2*

%files devel
%defattr(-,root,root,-)
%{_includedir}/openjpeg.h
%{_includedir}/openjpeg/
%{_libdir}/libopenjpeg.so

