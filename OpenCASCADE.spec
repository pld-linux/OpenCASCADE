#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# NOTE: there are some not PLD-relevant patches available:
#	- MIPS: http://git.debian.org/?p=debian-science/packages/opencascade.git;a=blob;f=debian/patches/fix-asm.patch
#	- kFreeBSD/Hurd: http://git.debian.org/?p=debian-science/packages/opencascade.git;a=blob;f=debian/patches/fix-osd_path.patch

# TODO: separate libs-x (80% of libraries)

Summary:	OpenCASCADE CAE platform
Name:		OpenCASCADE
# The 6.3.1 is a maintenance release, only available for OCC customers
Version:	6.3.0
Release:         40.3
License:	LGPL-like, see http://www.opencascade.org/occ/license/
Group:		Applications/Engineering
Source0:	http://files.opencascade.com/OCC_6.3_release/%{name}_src.tgz
# Source0-md5:	52778127974cb3141c2827f9d40d1f11
Patch0:		%{name}6.3.0-obs-check.patch
Patch1:		%{name}6.3.0-strcmp.patch
Patch2:		%{name}6.3.0-occ6.3.0.patch
Patch3:		%{name}6.3.0-casroot.patch
Patch4:		wokstep_extract.patch
Patch5:          OpenCASCADE6.3.0-tkernel-ld.patch
Patch6:		%{name}6.3.0-mft-disable-mmap.patch
Patch7:		%{name}6.3.0-no-bitmaps-icon.patch
Patch8:		%{name}6.3.0-DESTDIR.patch
Patch9:          OpenCASCADE6.3.0-maint-mode.patch
Patch10:         OpenCASCADE6.3.0-dep-libs.patch
Patch11:	%{name}6.3.0-move-vrml-vis.patch
Patch12:	%{name}6.3.0-make-wok-libs-private.patch
Patch13:	%{name}6.3.0-make-draw-libs-private.patch
Patch14:         OpenCASCADE6.3.0-wok-install.patch
Patch15:	%{name}6.3.0-udlist.patch
Patch16:	%{name}6.3.0-WOKUnix_FDescr.patch
Patch17:	fix-tklcaf.patch
URL:		http://www.opencascade.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
%ifnarch i486
BuildRequires:	java-sun-jdk-base
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	Mesa-libGLU-devel
BuildRequires:	tk-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-proto-xproto-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenCASCADE is a suite for 3D surface and solid modeling, visualization, data
exchange and rapid application development.  It is an excellent platform for
development of numerical simulation software including CAD/CAM/CAE, AEC and
GIS, as well as PDM applications.

%package libs
Summary:	OpenCASCADE shared libraries
Group:		Libraries

%description libs
OpenCASCADE shared libraries.

%package devel
Summary:	OpenCASCADE development files
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
OpenCASCADE development files.

%package doc
Summary:	OpenCASCADE documentation
Group:		Documentation

%description doc
OpenCASCADE help and html documentation.

%package samples
Summary:	OpenCASCADE samples
Group:		Documentation

%description samples
OpenCASCADE samples.

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
%patch17 -p1
cd ros/src/ExprIntrp
bison -d -p ExprIntrp -o ExprIntrp.tab.c ExprIntrp.yacc
flex -L -8 -Cf -Cr -P ExprIntrp -o lex.ExprIntrp.c ExprIntrp.lex
mv ExprIntrp.tab.h ../../inc/
cp ExprIntrp.tab.c lex.ExprIntrp.c ../../drv/ExprIntrp/

%build
cd ros
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%ifarch x86_64 ppc64
export CFLAGS="%{rpmcflags} -D_OCC64 -fno-strict-aliasing"
export CXXFLAGS="%{rpmcflags} -D_OCC64 -fno-strict-aliasing"
%else
export CFLAGS="%{rpmcflags} -fno-strict-aliasing"
export CXXFLAGS="%{rpmcflags} -fno-strict-aliasing"
%endif
LDFLAGS=-lpthread %configure \
	%{?debug:--disable-production  --enable-debug} \
	%{!?debug:--enable-production --disable-debug} \
	--with-java-include="%{java_home}"/include

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_includedir}}

cd ros
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..

cp -a data $RPM_BUILD_ROOT%{_datadir}/%{name}
mv $RPM_BUILD_ROOT{%{_prefix}/{src,wok,config.h,env_DRAW.sh},%{_datadir}/%{name}}
mv $RPM_BUILD_ROOT{%{_prefix}/inc,%{_includedir}/%{name}}
rm -r $RPM_BUILD_ROOT%{_prefix}/{Linux,lin}

mkdir -p $RPM_BUILD_ROOT/usr/src
for i in doc samples; do
mkdir -p $i-i
[ -d $i ] && mv $i $i-i/%{name}-%{version} || :
done
ln -s %{_builddir}/%{name}%{version}/doc-i   $RPM_BUILD_ROOT%{_defaultdocdir}
ln -s %{_builddir}/%{name}%{version}/samples-i $RPM_BUILD_ROOT%{_examplesdir}

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/DRAWEXE
%attr(755,root,root) %{_bindir}/wok*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/config.h
%{_datadir}/%{name}/data
%attr(755,root,root) %{_datadir}/%{name}/env_DRAW.sh
%dir %{_datadir}/%{name}/src
%dir %{_datadir}/%{name}/src/UnitsAPI
%{_datadir}/%{name}/src/UnitsAPI/*.dat
%{_datadir}/%{name}/wok
%dir %{_libdir}/opencas
%attr(755,root,root) %{_libdir}/opencas/*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/opencas/*.so.0

%files libs
%defattr(644,root,root,755)
%doc LICENSE ros/README.txt
%attr(755,root,root) %{_libdir}/*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/*.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
%{_libdir}/opencas/*.la
%{_libdir}/*.la
%attr(755,root,root) %{_libdir}/opencas/*.so
%attr(755,root,root) %{_libdir}/*.so
%{_datadir}/%{name}/src/*
%exclude %{_datadir}/%{name}/src/UnitsAPI/*.dat

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}-%{version}

%files samples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
