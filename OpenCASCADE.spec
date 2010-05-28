#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

Summary:	OpenCASCADE CAE platform
Name:		OpenCASCADE
Group:           Productivity/Other
# The 6.3.1 is a maintenance release, only available for OCC customers
Version:	6.3.0
Release:         40.3
License:	LGPL-like, see http://www.opencascade.org/occ/license/
Packager:        Andrea Florio <andrea@opensuse.org>
Source0:	http://files.opencascade.com/OCC_6.3_release/%{name}_src.tgz
# Source0-md5:	52778127974cb3141c2827f9d40d1f11
Source1:	 %name.conf
Source2:	 OpenCASCADE-rpmlintrc
Patch0:		%{name}6.3.0-obs-check.patch
Patch1:		%{name}6.3.0-strcmp.patch
Patch2:          OpenCASCADE6.3.0-occ6.3.0.patch
Patch3:          OpenCASCADE6.3.0-casroot.patch
Patch4:          OpenCASCADE6.3.0-lib-release.patch
Patch5:          OpenCASCADE6.3.0-tkernel-ld.patch
Patch6:          OpenCASCADE6.3.0-mft-disable-mmap.patch
Patch7:          OpenCASCADE6.3.0-no-bitmaps-icon.patch
Patch8:		%{name}6.3.0-DESTDIR.patch
Patch9:          OpenCASCADE6.3.0-maint-mode.patch
Patch10:         OpenCASCADE6.3.0-dep-libs.patch
Patch11:         OpenCASCADE6.3.0-move-vrml-vis.patch
Patch12:         OpenCASCADE6.3.0-make-wok-libs-private.patch
Patch13:         OpenCASCADE6.3.0-make-draw-libs-private.patch
Patch14:         OpenCASCADE6.3.0-wok-install.patch
Patch15:         OpenCASCADE6.3.0-udlist.patch
Patch16:         OpenCASCADE6.3.0-WOKUnix_FDescr.patch
URL:		http://www.opencascade.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	java-sun-jdk-base
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	Mesa-libGLU-devel
BuildRequires:	tk-devel
BuildRequires:  bison flex tcl-devel tk-devel
%ifarch i586
BuildRequires:   compat
%else
BuildRequires:   compat-32bit
%endif
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-proto-xproto-devel
Requires:        tcsh
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenCASCADE is a suite for 3D surface and solid modeling, visualization, data
exchange and rapid application development.  It is an excellent platform for
development of numerical simulation software including CAD/CAM/CAE, AEC and
GIS, as well as PDM applications.

%package devel
Group:          Development/Libraries/C and C++
Summary:        Devel package for %{name}
Requires:       %{name} = %{version}

%description devel
OpenCASCADE is a suite for 3D surface and solid modeling, visualization, data
exchange and rapid application development.  It is an excellent platform for
development of numerical simulation software including CAD/CAM/CAE, AEC and
GIS, as well as PDM applications.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1

%build
cd ros
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

cd ros/src/ExprIntrp
bison -d -p ExprIntrp -o ExprIntrp.tab.c ExprIntrp.yacc
flex -L -8 -Cf -Cr -P ExprIntrp -o lex.ExprIntrp.c ExprIntrp.lex
mv ExprIntrp.tab.h ../../inc/
cp ExprIntrp.tab.c lex.ExprIntrp.c ../../drv/ExprIntrp/
cd ../..
%ifarch x86_64 ppc64
export CFLAGS="$RPM_OPT_FLAGS -D_OCC64 -fno-strict-aliasing"
export CXXFLAGS="$RPM_OPT_FLAGS -D_OCC64 -fno-strict-aliasing"
%else
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%endif
LDFLAGS=-lpthread %configure \
   --disable-static \
   --disable-debug \
   --enable-production \
   --enable-draw \
   --enable-wok \
   --enable-wrappers \
	--with-java-include=/usr/lib64/jvm/java/include

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd ros
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd ..
cp -a data %{buildroot}%{_prefix}/
cp -a doc %{buildroot}%{_prefix}/
cp -a samples %{buildroot}%{_prefix}/

%ifarch x86_64
%__ln_s %{_libdir} %{buildroot}/%{_prefix}/Linux/lib
%__ln_s %{_libdir} %{buildroot}/%{_prefix}/lin/lib
%endif

# add symlinks for compatibility resons
%__mkdir -p %{buildroot}/usr/share/opencascade/
%__mkdir -p %{buildroot}/usr/include/
%__mkdir -p %{buildroot}/usr/share/doc/packages/
%__mkdir -p %{buildroot}/usr/%{_lib}

%__ln_s %{_prefix} %{buildroot}/usr/share/opencascade/%{version}
%__ln_s %{_prefix}/inc  %{buildroot}/usr/include/opencascade
%__ln_s %{_prefix}/doc  %{buildroot}/usr/share/doc/packages/opencascade
`for i in $(ls  %{buildroot}/%{_libdir}); do %__ln_s %{_libdir}/$i %{buildroot}/usr/%{_lib}/$i; done`

%__mkdir -p %buildroot/etc/ld.so.conf.d/
%__cp %SOURCE1 %buildroot/etc/ld.so.conf.d/

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_prefix}
%dir %{_bindir}
%dir %{_prefix}/lin
%dir %{_prefix}/Linux
%dir %{_prefix}/wok
%dir %{_prefix}/wok/lib/
%dir %{_prefix}/wok/site/
%dir %{_prefix}/data
%dir %{_prefix}/doc
%dir %{_libdir}/
%dir %{_libdir}/opencas/
%dir /usr/share/opencascade/
%{_bindir}/DRAWEXE
%{_bindir}/wokprocess
%{_bindir}/woksh
%{_prefix}/lin/bin
%{_prefix}/lin/lib
%{_prefix}/Linux/bin
%{_prefix}/Linux/lib
%{_prefix}/data/*
%{_prefix}/doc/*
%{_prefix}/wok/lib/*
%{_prefix}/wok/site/*
%{_prefix}/config.h
%{_prefix}/env_DRAW.sh
%{_libdir}/*.so
%{_libdir}/opencas/*.so
/usr/%_lib/*
/usr/share/opencascade/%{version}
/usr/share/doc/packages/opencascade
%config /etc/ld.so.conf.d/%name.conf
%dir %{_prefix}/src/UnitsAPI
%dir %{_prefix}/src
%{_prefix}/src/UnitsAPI/*.dat

%files devel
%defattr(644,root,root,755)
%dir /usr/include/opencascade/
%{_libdir}/*.la
%{_libdir}/opencas/*.la
%dir %{_prefix}/src/
%{_prefix}/src/*
%dir %{_prefix}/inc/
%{_prefix}/inc/*
%dir %{_prefix}/samples
%{_prefix}/samples/*
%exclude %{_prefix}/src/UnitsAPI/*.dat
