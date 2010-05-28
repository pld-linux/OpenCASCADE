#
# spec file for package OpenCASCADE
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# norootforbuild

%define _prefix /opt/OpenCASCADE

Name:            OpenCASCADE
Summary:    	 OpenCASCADE CAE platform
Url:             http://www.opencascade.org/
Group:           Productivity/Other
Version:         6.3.0
Release:         40.3
License:         LGPL-like, see http://www.opencascade.org/occ/license/
Packager:        Andrea Florio <andrea@opensuse.org>
Source0:         %{name}%{version}.tar.bz2
Source1:	 %name.conf
Source2:	 OpenCASCADE-rpmlintrc
Patch0:          OpenCASCADE6.3.0-obs-check.patch
Patch1:          OpenCASCADE6.3.0-strcmp.patch
Patch2:          OpenCASCADE6.3.0-occ6.3.0.patch
Patch3:          OpenCASCADE6.3.0-casroot.patch
Patch4:          OpenCASCADE6.3.0-lib-release.patch
Patch5:          OpenCASCADE6.3.0-tkernel-ld.patch
Patch6:          OpenCASCADE6.3.0-mft-disable-mmap.patch
Patch7:          OpenCASCADE6.3.0-no-bitmaps-icon.patch
Patch8:          OpenCASCADE6.3.0-DESTDIR.patch
Patch9:          OpenCASCADE6.3.0-maint-mode.patch
Patch10:         OpenCASCADE6.3.0-dep-libs.patch
Patch11:         OpenCASCADE6.3.0-move-vrml-vis.patch
Patch12:         OpenCASCADE6.3.0-make-wok-libs-private.patch
Patch13:         OpenCASCADE6.3.0-make-draw-libs-private.patch
Patch14:         OpenCASCADE6.3.0-wok-install.patch
Patch15:         OpenCASCADE6.3.0-udlist.patch
Patch16:         OpenCASCADE6.3.0-WOKUnix_FDescr.patch

BuildRequires:   Mesa-devel autoconf automake bison gcc-c++ xorg-x11-devel
BuildRequires:   flex libtool tcl-devel tk-devel xorg-x11-libXmu-devel fdupes
%ifarch i586
BuildRequires:   compat
%else
BuildRequires:   compat-32bit
%endif
%if %suse_version >= 1100
BuildRequires:   java-1_5_0-gcj-compat-devel
%else
BuildRequires:   java-1_4_2-gcj-compat-devel
%endif
Requires:        tcsh
BuildRoot:       %{_tmppath}/%{name}-%{version}-build

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
# all patches must applied in that order or some of them could fail
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
autoreconf -f -i
LDFLAGS=-lpthread %configure \
   --with-gl-include=/usr/include \
   --with-gl-library=/usr/%{_lib} \
   --with-xmu-include=/usr/include/X11 \
   --with-xmu-library=/usr/%{_lib} \
   --with-tcl=/usr/%{_lib} \
   --with-tk=/usr/%{_lib} \
   --disable-static \
   --disable-debug \
   --enable-production \
   --enable-wok \
   --enable-wrappers \
   --enable-draw

%__make %{?jobs:-j%{jobs}}

%install
cd ros
%makeinstall

`for i in $(find %{buildroot}%{_prefix}/inc/ -name '*.h'); do chmod -x $i; done`
`for i in $(find %{buildroot}%{_prefix}/inc/ -name '*.hxx'); do chmod -x $i; done`
`for i in $(find %{buildroot}%{_prefix}/inc/ -name '*.lxx'); do chmod -x $i; done`
`for i in $(find %{buildroot}%{_prefix}/inc/ -name '*.gxx'); do chmod -x $i; done`

chmod -x %{buildroot}%{_prefix}/wok/lib/config.h
chmod -x %{buildroot}%{_libdir}/*.la
chmod -x %{buildroot}%{_libdir}/opencas/*.la
chmod -x %{buildroot}%{_prefix}/src/UnitsAPI/UnitsAPI.cxx
chmod -x %{buildroot}%{_prefix}/src/DrawResources/Filtre.c
chmod -x %{buildroot}%{_prefix}/src/DrawResources/TestDraw.cxx
chmod -x %{buildroot}%{_prefix}/src/DrawResources/DIFF.c

cd ..
mv data %{buildroot}%{_prefix}/
mv doc %{buildroot}%{_prefix}/
mv samples %{buildroot}%{_prefix}/
find %{buildroot}%{_prefix}/data -type f -print0 |xargs -0 chmod a-x
find %{buildroot}%{_prefix}/doc -type f -print0 |xargs -0 chmod a-x
find %{buildroot}%{_prefix}/samples -type f -print0 |xargs -0 chmod a-x

%ifarch x86_64
%__ln_s %{_libdir} %{buildroot}/%{_prefix}/Linux/lib
%__ln_s %{_libdir} %{buildroot}/%{_prefix}/lin/lib
%endif

# add synlinks for compatibility resons
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

%fdupes -s %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
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
%defattr(-,root,root)
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

%changelog
* Fri Dec  4 2009 andrea@opensuse.org
- enabled wrappers
* Sat May  2 2009 andrea@opensuse.org
- added some symlink to provide compatibility with soma packages
* Tue Feb 10 2009 andrea@opensuse.org
- moved *.dat to main package, not sources and some packages need them
* Wed Oct 29 2008 lars@linux-schulserver.de
- ignore post-build-checks until /opt is allowed again
* Sat Sep 27 2008 Andrea Florio <andrea@opensuse.org> 6.3.0
- new package
