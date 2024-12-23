#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# TODO: - separate libs-x (80% of libraries), follow Fedora split or split packages as suggested by Jason Kraftcheck in Debian

# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	draco		# Draco compression support
%bcond_with	ffmpeg		# FFmpeg support, needs ffmpeg < 5
%bcond_without	freeimage	# FreeImage support
%bcond_without	openvr		# OpenVR support
%bcond_without	qt		# Qt based inspector
%bcond_without	tbb		# TBB support
%bcond_without	vtk		# VTK toolkit

Summary:	OpenCASCADE CAE platform
Summary(pl.UTF-8):	Platforma CAE OpenCASCADE
Name:		OpenCASCADE
Version:	7.8.1
%define	tagver	%(echo %{version} | tr . _)
Release:	1
License:	LGPL v2.1 with Open CASCADE Exception v1.0
Group:		Applications/Engineering
#Source0Download https://dev.opencascade.org/release
Source0:	https://github.com/Open-Cascade-SAS/OCCT/archive/V%{tagver}/OCCT-%{tagver}.tar.gz
# Source0-md5:	a1ae2c20422dd7a4352758667f34851f
Patch0:		%{name}-cmake.patch
Patch1:		%{name}-inspector-data.patch
Patch2:		%{name}-draco.patch
Patch3:		%{name}-openvr.patch
Patch4:		%{name}-X.patch
Patch5:		cmake-libdir.patch
Patch6:		strict-const.patch
URL:		https://www.opencascade.com/open-cascade-technology/
%{?with_freeimage:BuildRequires:	FreeImage-devel}
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	bison
BuildRequires:	cmake >= 3.1
BuildRequires:	doxygen >= 1:1.8.4
%{?with_draco:BuildRequires:	draco-devel}
BuildRequires:	eigen3
# avcodec avformat avutil swscale
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel}
BuildRequires:	flex
BuildRequires:	freetype-devel >= 2
%ifnarch i386 i486
BuildRequires:	jdk
%endif
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool
%{?with_openvr:BuildRequires:	openvr-devel}
BuildRequires:	rapidjson-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
%{?with_tbb:BuildRequires:	tbb-devel >= 2021.4}
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
%{?with_vtk:BuildRequires:	vtk-devel}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-proto-xproto-devel
%if %{with qt}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Quick-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	Qt5Xml-devel >= 5
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-linguist >= 5
%endif
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	inkscape
BuildRequires:	texlive-pdftex
%endif
Requires:	%{name}-libs = %{version}-%{release}
%{?with_tbb:Requires:	tbb >= 2021.4}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautocompressdoc	*.chm

%description
OpenCASCADE is a suite for 3D surface and solid modeling,
visualization, data exchange and rapid application development. It is
an excellent platform for development of numerical simulation software
including CAD/CAM/CAE, AEC and GIS, as well as PDM applications.

%description -l pl.UTF-8
OpenCASCADE to szkielet do modelowania powierzchni i brył 3D wraz z
wizualizacją, wymianą danych i wsparciem szybkiego tworzenia
aplikacji. Jest to świetna platforma do rozwoju oprogramowania
symulacji numerycznych, w tym CAD/CAM/CAE, AEC oraz GIS, a także
aplikacji PDM.

%package libs
Summary:	OpenCASCADE shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone OpenCASCADE
Group:		Libraries

%description libs
OpenCASCADE shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone OpenCASCADE.

%package devel
Summary:	OpenCASCADE development files
Summary(pl.UTF-8):	Pliki programistyczne OpenCASCADE
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel
# for CommandWindow.h
Requires:	tcl-devel

%description devel
OpenCASCADE development files.

%description devel -l pl.UTF-8
Pliki programistyczne OpenCASCADE.

%package inspector
Summary:	OCCT Inspector application
Summary(pl.UTF-8):	Aplikacja OCCT Inspector
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-inspector-libs = %{version}-%{release}

%description inspector
OCCT Inspector application.

%description inspector -l pl.UTF-8
Aplikacja OCCT Inspector.

%package inspector-libs
Summary:	OCCT Inspector libraries
Summary(pl.UTF-8):	Biblioteki OCCT Inspector
Group:		X11/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description inspector-libs
OCCT Inspector libraries.

%description inspector-libs -l pl.UTF-8
Biblioteki OCCT Inspector.

%package inspector-devel
Summary:	Header files for OCCT Inspector libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek OCCT Inspector
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-inspector-libs = %{version}-%{release}
Requires:	Qt5Core-devel >= 5
Requires:	Qt5Gui-devel >= 5
Requires:	Qt5Widgets-devel >= 5
Requires:	Qt5Xml-devel >= 5

%description inspector-devel
Header files for OCCT Inspector libraries.

%description inspector-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek OCCT Inspector.

%package vtk
Summary:	OCCT VTK libraries
Summary(pl.UTF-8):	Biblioteki OCCT VTK
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description vtk
OCCT VTK libraries.

%description vtk -l pl.UTF-8
Biblioteki OCCT VTK.

%package vtk-devel
Summary:	Header files for OCCT VTK libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek OCCT VTK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-vtk = %{version}-%{release}
Requires:	vtk-devel

%description vtk-devel
Header files for OCCT VTK libraries.

%description vtk-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek OCCT VTK.

%package doc
Summary:	OpenCASCADE documentation
Summary(pl.UTF-8):	Dokumentacja do OpenCASCADE
Group:		Documentation
BuildArch:	noarch

%description doc
OpenCASCADE help and HTML documentation.

%description doc -l pl.UTF-8
Pomoc oraz dokumentacja w formacie HTML do OpenCASCADE.

%package samples
Summary:	OpenCASCADE samples
Summary(pl.UTF-8):	Przykłady do OpenCASCADE
Group:		Documentation
BuildArch:	noarch

%description samples
OpenCASCADE samples.

%description samples -l pl.UTF-8
Przykłady do OpenCASCADE.

%prep
%setup -q -n OCCT-%{tagver}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1
%patch -P 6 -p1

%{__sed} -i -e '/set (CMAKE_CONFIGURATION_TYPES/ { s/INTERNAL/STRING/;s/ FORCE// }' CMakeLists.txt
%{__sed} -i -e 's/IMPORTED_LOCATION_RELEASE/IMPORTED_LOCATION_PLD/' adm/cmake/tbb.cmake

%build
install -d build
cd build
# vtk defines GL_GLEXT_LEGACY; occt uses <GL/glx.h>, so set GLX_GLXEXT_LEGACY for consistency
CXXFLAGS="%{rpmcxxflags} -DNDEBUG -DQT_NO_DEBUG -DGLX_GLXEXT_LEGACY=1"
%cmake .. \
	-D3RDPARTY_DRACO_INCLUDE_DIR=%{_includedir}/draco \
	-D3RDPARTY_DRACO_LIBRARY=%{_libdir}/libdraco.so \
	-D3RDPARTY_OPENVR_INCLUDE_DIR=%{_includedir}/openvr \
	%{?with_qt:-D3RDPARTY_QT_DIR=/usr} \
	%{?with_qt:-DBUILD_Inspector=ON} \
	-DBUILD_YACCLEX=ON \
	-DCMAKE_CONFIGURATION_TYPES=%{?debug:Debug}%{!?debug:PLD} \
	-DINSTALL_DIR_CMAKE=%{_lib}/cmake/opencascade \
	-DINSTALL_DIR_LIB=%{_lib} \
	%{?with_draco:-DUSE_DRACO=ON} \
	-DUSE_EIGEN=ON \
	%{?with_ffmpeg:-DUSE_FFMPEG=ON} \
	%{?with_freeimage:-DUSE_FREEIMAGE=ON} \
	%{?with_openvr:-DUSE_OPENVR=ON} \
	-DUSE_RAPIDJSON=ON \
	%{?with_tbb:-DUSE_TBB=ON} \
	-D3RDPARTY_VTK_INCLUDE_DIR=/usr/include/vtk \
	%{?with_vtk:-DUSE_VTK=ON}

# CMAKE_VERBOSE_MAKEFILE seems to be ignored
%{__make} \
	VERBOSE=1

cd ..

%if %{with apidocs}
./gendoc -overview -html
./gendoc -refman -html
%{__rm} doc/refman/OCCT.{dox,tag}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{DRAWEXE-%{version},DRAWEXE}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{ExpToCasExe-%{version},ExpToCasExe}
%if %{with qt}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{TInspectorEXE-%{version},TInspectorEXE}
%endif

# names are too common to keep in %{_bindir}
# also, the files are to be sourced, not executed
install -d $RPM_BUILD_ROOT%{_libdir}/opencascade
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{env,custom*}.sh $RPM_BUILD_ROOT%{_libdir}/opencascade
%{__sed} -i -e 's,\${CASROOT}/bin/custom.sh,${aScriptPath}/custom.sh,' $RPM_BUILD_ROOT%{_libdir}/opencascade/env.sh
# adjust paths
%{__sed} -i -e 's,^aScriptPath=.*,aScriptPath=%{_libdir}/opencascade,' \
	$RPM_BUILD_ROOT%{_bindir}/draw.sh \
	%{?with_qt:$RPM_BUILD_ROOT%{_bindir}/inspector.sh}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr samples/{OCCTOverview,glfw,ocafsamples,qt,tcl,webgl,xaml} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# just LGPL v2.1 copy
%{__rm} $RPM_BUILD_ROOT%{_docdir}/opencascade/LICENSE_LGPL_21.txt
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/opencascade/OCCT_LGPL_EXCEPTION.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post   inspector-libs -p /sbin/ldconfig
%postun inspector-libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/DRAWEXE
# R: libTKExpress libTKernel
%attr(755,root,root) %{_bindir}/ExpToCasExe
%attr(755,root,root) %{_bindir}/draw.sh
%dir %{_datadir}/opencascade
%{_datadir}/opencascade/data
%{_datadir}/opencascade/resources

%files libs
%defattr(644,root,root,755)
%doc OCCT_LGPL_EXCEPTION.txt README.txt
# R: libTKBRep libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKPrim libTKShHealing libTKTopAlgo libTKernel
%attr(755,root,root) %{_libdir}/libTKBO.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKBO.so.7.8
# R: libTKG2d libTKG3d libTKGeomBase libTKMath libTKernel
%attr(755,root,root) %{_libdir}/libTKBRep.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKBRep.so.7.8
# R: libTKBRep libTKBinL libTKCAF libTKCDF libTKLCAF libTKMath libTKernel
%attr(755,root,root) %{_libdir}/libTKBin.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKBin.so.7.8
# R: libTKCDF libTKLCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKBinL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKBinL.so.7.8
# R: libTKBinL libTKCDF libTKLCAF libTKTObj libTKernel
%attr(755,root,root) %{_libdir}/libTKBinTObj.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKBinTObj.so.7.8
# R: libTKBRep libTKBin libTKBinL libTKCAF libTKCDF libTKLCAF libTKMath libTKService libTKXCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKBinXCAF.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKBinXCAF.so.7.8
# R: libTKBO libTKBRep libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKPrim libTKShHealing libTKTopAlgo libTKernel
%attr(755,root,root) %{_libdir}/libTKBool.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKBool.so.7.8
# R: libGKBO libTKBRep libTKCDF libTKG3d libTKGeomBase libTKLCAF libTKMath libTKTopAlgo libTKernel
%attr(755,root,root) %{_libdir}/libTKCAF.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKCAF.so.7.8
# R: libTKernel
%attr(755,root,root) %{_libdir}/libTKCDF.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKCDF.so.7.8
# R: libTKBO libTKBRep libTKBin libTKBinL libTKBool libTKCAF libTKCDF libTKDraw libTKFillet libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKLCAF libTKMath libTKPrim libTKStd libTKStdL libTKTopAlgo libTKV3d libTKVCAF libTKViewerTest libTKXml libTKXmlL libTKernel
%attr(755,root,root) %{_libdir}/libTKDCAF.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKDCAF.so.7.8
# R: libTKernel
%attr(755,root,root) %{_libdir}/libTKDE.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKDE.so.7.8
# R: libTKBRep libTKBin libTKBinL libTKBinTObj libTKBinXCAF libTKCDF libTKDE libTKLCAF libTKMath libTKStd libTKStdL libTKXCAF libTKXml libTKXmlL libTKXmlTObj libTKXmlTObj libTKXmlXCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKDECascade.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKDECascade.so.7.8
# R: libTKBRep libTKDE libTKG3d libTKLCAF libTKMath libTKRWMesh libTKService libTKXCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKDEGLTF.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKDEGLTF.so.7.8
# R: libTKBRep libTKBool libTKDE libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKLCAF libTKMath libTKPrim libTKShHealing libTKTopAlgo libTKXCAF libTKXSBase libTKernel %{?with_draco:draco}
%attr(755,root,root) %{_libdir}/libTKDEIGES.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKDEIGES.so.7.8
# R: libTKBRep libTKDE libTKG3d libTKLCAF libTKMath libTKMesh libTKRWMesh libTKService libTKXCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKDEOBJ.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKDEOBJ.so.7.8
# R: libTKBRep libTKDE libTKG3d libTKLCAF libTKMath libTKRWMesh libTKXCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKDEPLY.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKDEPLY.so.7.8
# R: libTKBRep libTKDE libTKG2d libTKG3d libTKGeomBase libTKLCAF libTKMath libTKShHealing libTKTopAlgo libTKXCAF libTKXSBase libTKernel
%attr(755,root,root) %{_libdir}/libTKDESTEP.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKDESTEP.so.7.8
# R: libTKBRep libTKDE libTKLCAF libTKMath libTKTopAlgo libTKXCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKDESTL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKDESTL.so.7.8
# R: libTKBRep libTKDE libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKHLR libTKLCAF libTKMath libTKMesh libTKPrim libTKRWMesh libTKTopAlgo libTKV3d libTKXCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKDEVRML.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKDEVRML.so.7.8
# R: libTKBRep libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKHLR libTKMath libTKMesh libTKService libTKTopAlgo libTKernel libX11 tcl tk
%attr(755,root,root) %{_libdir}/libTKDraw.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKDraw.so.7.8
# R: libTKernel
%attr(755,root,root) %{_libdir}/libTKExpress.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKExpress.so.7.8
# R: libTKBO libTKBRep libTKBool libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKPrim libTKShHealing libTKTopAlgo libTKernel
%attr(755,root,root) %{_libdir}/libTKFeat.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKFeat.so.7.8
# R: libTKBO libTKBRep libTKBool libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKShHealing libTKTopAlgo libTKernel
%attr(755,root,root) %{_libdir}/libTKFillet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKFillet.so.7.8
# R: libTKMath libTKernel
%attr(755,root,root) %{_libdir}/libTKG2d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKG2d.so.7.8
# R: libTKG2d libTKMath libTKernel
%attr(755,root,root) %{_libdir}/libTKG3d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKG3d.so.7.8
# R: libTKBRep libTKG2d libTKG3d libTKGeomBase libTKMath libTKernel
%attr(755,root,root) %{_libdir}/libTKGeomAlgo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKGeomAlgo.so.7.8
# R: libTKG2d libTKG3d libTKMath libTKernel
%attr(755,root,root) %{_libdir}/libTKGeomBase.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKGeomBase.so.7.8
# R: libTKBRep libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKTopAlgo libTKernel
%attr(755,root,root) %{_libdir}/libTKHLR.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKHLR.so.7.8
# R: libTKCDF libTKernel
%attr(755,root,root) %{_libdir}/libTKLCAF.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKLCAF.so.7.8
# R: libTKernel
%attr(755,root,root) %{_libdir}/libTKMath.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKMath.so.7.8
# R: libTKBrep libTKG2d libTKG3d libTKGeomBase libTKMath libTKShHealing libTKTopAlgo libTKernel
%attr(755,root,root) %{_libdir}/libTKMesh.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKMesh.so.7.8
# R: libTKMath libTKService libTKV3d libTKernel
%attr(755,root,root) %{_libdir}/libTKMeshVS.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKMeshVS.so.7.8
# R: libTKBO libTKBRep libTKBool libTKFillet libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKPrim libTKShHealing libTKTopAlgo libTKernel
%attr(755,root,root) %{_libdir}/libTKOffset.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKOffset.so.7.8
# R: libTKMath libTKService libTKernel libGL libX11
%attr(755,root,root) %{_libdir}/libTKOpenGl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKOpenGl.so.7.8
# R: libTKDraw libTKOpenGl libTKService libTKV3d libTKViewerTest libTKernel
%attr(755,root,root) %{_libdir}/libTKOpenGlTest.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKOpenGlTest.so.7.8
# R: libTKBRep libTKG2d libTKG3d libTKGeomBase libTKMath libTKTopAlgo libTKernel
%attr(755,root,root) %{_libdir}/libTKPrim.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKPrim.so.7.8
# R: libTKBO libTKBRep libTKBin libTKBinL libTKBinXCAF libTKBool libTKCAF libTKCDF libTKDCAF libTKDEIGES libTKDESTEP libTKDraw libTKFeat libTKFillet libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKHLR libTKLCAF libTKMath libTKMesh libTKOffset libTKPrim libTKService libTKShHealing libTKStd libTKStdL libTKTObj libTKTopAlgo libTKV3d libTKVCAF libTKViewerTest libTKXCAF libTKXSBase libTKXml libTKXmlL libTKernel %{?with_tbb:tbb}
%attr(755,root,root) %{_libdir}/libTKQADraw.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKQADraw.so.7.8
# R: libTKBRep libTKG3d liBTKLCAF libTKMath libTKService libTKXCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKRWMesh.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKRWMesh.so.7.8
# R: libTKMath libTKernel libX11 fontconfig freetype %{?with_freeimage:FreeImage} %{?with_ffmpeg:ffmpeg-libs} %{?with_openvr:openvr}
%attr(755,root,root) %{_libdir}/libTKService.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKService.so.7.8
# R: libTKBrep libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKTopAlgo libTKernel
%attr(755,root,root) %{_libdir}/libTKShHealing.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKShHealing.so.7.8
# R: libTKBRep libTKCAF libTKCDF libTKG2d libG3d libGKLCAF libTKMath libTKStdL libTKernel
%attr(755,root,root) %{_libdir}/libTKStd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKStd.so.7.8
# R: libTKCDF libTKLCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKStdL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKStdL.so.7.8
# R: libTKCDF libTKLCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKTObj.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKTObj.so.7.8
# R: libTKBinTObj libTKDCAF libTKDraw libTKLCAF libTKTObj libTKXmlTObj libTKernel
%attr(755,root,root) %{_libdir}/libTKTObjDRAW.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKTObjDRAW.so.7.8
# R: libTKBRep libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKernel
%attr(755,root,root) %{_libdir}/libTKTopAlgo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKTopAlgo.so.7.8
# R: libTKBO libTKBRep libTKBool libTKDraw libTKFeat libTKFillet libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKHLR libTKMath libTKMesh libTKOffset libTKPrim libTKShHealing libTKTopAlgo libTKV3d libTKernel
%attr(755,root,root) %{_libdir}/libTKTopTest.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKTopTest.so.7.8
# R: libTKBRep liBTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKHLR libTKMath libTKMesh libTKService libTKTopAlgo libTKernel
%attr(755,root,root) %{_libdir}/libTKV3d.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKV3d.so.7.8
# R: libTKBRep libTKCAF libTKG3d libTKGeomBase libTKLCAF libTKMath libTKService libTKTopAlgo libTKV3d libTKernel
%attr(755,root,root) %{_libdir}/libTKVCAF.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKVCAF.so.7.8
# R: libTKBRep libTKDraw libTKFillet libTKG3d libTKGeomAlgo libTKGeomBase libTKHLR libTKMath libTKService libTKTopAlgo libTKV3d libTKernel libX11 tcl
%attr(755,root,root) %{_libdir}/libTKViewerTest.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKViewerTest.so.7.8
# R: libTKBRep libTKCAF libTKCDF libTKG3d libTKLCAF libTKMath libTKService libTKTopAlgo libTKV3d libTKVCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKXCAF.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXCAF.so.7.8
# R: libTKBRep libTKBinXCAF libTKCAF libTKCDF libTKDCAF libTKDESTEP libTKDraw libTKG3d libTKLCAF libTKMath libTKMesh libTKService libTKTopAlgo libTKV3d libTKVCAF libTKViewerTest libTKXCAF libTKXSBase libTKXSDRAW libTKXmlXCAF libTKernel
%attr(755,root,root) %{_libdir}/libTKXDEDRAW.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXDEDRAW.so.7.8
# R: libTKMath libTKMesh libTKernel
%attr(755,root,root) %{_libdir}/libTKXMesh.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXMesh.so.7.8
# R: libTKBRep libTKG2d libTKG3d libTKMath libTKShHealing libTKTopAlgo libTKernel
%attr(755,root,root) %{_libdir}/libTKXSBase.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXSBase.so.7.8
# R: libTKDraw libTKG2d libTKG3d libTKXCAF libTKXSBase libTKernel
%attr(755,root,root) %{_libdir}/libTKXSDRAW.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXSDRAW.so.7.8
# R: libTKDCAF libTKDE libTKDECascade libTKDraw.so libTKLCAF libTKMath libTKXSDRAW libTKernel
%attr(755,root,root) %{_libdir}/libTKXSDRAWDE.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXSDRAWDE.so.7.8
# R: libTKDCAF libTKDEGLTF libTKDraw.so libTKLCAF libTKMath libTKRWMesh libTKXCAF libTKXSDRAW libTKernel
%attr(755,root,root) %{_libdir}/libTKXSDRAWGLTF.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXSDRAWGLTF.so.7.8
# R: libTKBRep libTKDCAF libTKDEIGES libTKDraw libTKLCAF libTKXSBase libTKXSDRAW libTKernel
%attr(755,root,root) %{_libdir}/libTKXSDRAWIGES.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXSDRAWIGES.so.7.8
# R: libTKBRep libTKDCAF libTKDEOBJ libTKDraw libTKLCAF libTKMath libTKRWMesh libTKXCAF libTKXSDRAW libTKernel
%attr(755,root,root) %{_libdir}/libTKXSDRAWOBJ.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXSDRAWOBJ.so.7.8
# R: libTKBRep libTKDCAF libTKDEPLY libTKDraw libTKG3d libTKLCAF libTKMath libTKRWMesh libTKTopAlgo libTKXCAF libTKXSDRAW libTKernel
%attr(755,root,root) %{_libdir}/libTKXSDRAWPLY.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXSDRAWPLY.so.7.8
# R: libTKDCAF libTKDESTEP libTKDraw libTKLCAF libTKMath libTKXSBase libTKXSDRAW libTKernel
%attr(755,root,root) %{_libdir}/libTKXSDRAWSTEP.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXSDRAWSTEP.so.7.8
# R: libTKBRep libTKDESTL libTKDraw libTKMath libTKMeshVS libTKService libTKV3d libTKViewerTest libTKXSDRAW libTKernel
%attr(755,root,root) %{_libdir}/libTKXSDRAWSTL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXSDRAWSTL.so.7.8
# R: libTKDCAF libTKDEVRML libTKDraw libTKLCAF libTKMath libTKRWMesh libTKXCAF libTKXSBase libTKXSDRAW libTKernel
%attr(755,root,root) %{_libdir}/libTKXSDRAWVRML.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXSDRAWVRML.so.7.8
# R: libTKBRep libTKCAF libTKCDF libTKLCAF libTKMath libTKXmlL libTKernel
%attr(755,root,root) %{_libdir}/libTKXml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXml.so.7.8
# R: libTKCDF libTKLCAF libTKMath libTKernel
%attr(755,root,root) %{_libdir}/libTKXmlL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXmlL.so.7.8
# R: R: libTKCDF libTKLCAF libTKTObj libTKXmlL libTKernel
%attr(755,root,root) %{_libdir}/libTKXmlTObj.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXmlTObj.so.7.8
# R: libTKBRep libTKCAF libTKCDF libTKLCAF libTKMath libTKService libTKXCAF libTKXml libTKXmlL libTKernel
%attr(755,root,root) %{_libdir}/libTKXmlXCAF.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKXmlXCAF.so.7.8
# R: (libstdc++) %{?with_tbb:tbb}
%attr(755,root,root) %{_libdir}/libTKernel.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKernel.so.7.8
%dir %{_libdir}/opencascade
%{_libdir}/opencascade/custom*.sh
%{_libdir}/opencascade/env.sh

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libTKBO.so
%attr(755,root,root) %{_libdir}/libTKBRep.so
%attr(755,root,root) %{_libdir}/libTKBin.so
%attr(755,root,root) %{_libdir}/libTKBinL.so
%attr(755,root,root) %{_libdir}/libTKBinTObj.so
%attr(755,root,root) %{_libdir}/libTKBinXCAF.so
%attr(755,root,root) %{_libdir}/libTKBool.so
%attr(755,root,root) %{_libdir}/libTKCAF.so
%attr(755,root,root) %{_libdir}/libTKCDF.so
%attr(755,root,root) %{_libdir}/libTKDCAF.so
%attr(755,root,root) %{_libdir}/libTKDE.so
%attr(755,root,root) %{_libdir}/libTKDECascade.so
%attr(755,root,root) %{_libdir}/libTKDEGLTF.so
%attr(755,root,root) %{_libdir}/libTKDEIGES.so
%attr(755,root,root) %{_libdir}/libTKDEOBJ.so
%attr(755,root,root) %{_libdir}/libTKDEPLY.so
%attr(755,root,root) %{_libdir}/libTKDESTEP.so
%attr(755,root,root) %{_libdir}/libTKDESTL.so
%attr(755,root,root) %{_libdir}/libTKDEVRML.so
%attr(755,root,root) %{_libdir}/libTKDraw.so
%attr(755,root,root) %{_libdir}/libTKExpress.so
%attr(755,root,root) %{_libdir}/libTKFeat.so
%attr(755,root,root) %{_libdir}/libTKFillet.so
%attr(755,root,root) %{_libdir}/libTKG2d.so
%attr(755,root,root) %{_libdir}/libTKG3d.so
%attr(755,root,root) %{_libdir}/libTKGeomAlgo.so
%attr(755,root,root) %{_libdir}/libTKGeomBase.so
%attr(755,root,root) %{_libdir}/libTKHLR.so
%attr(755,root,root) %{_libdir}/libTKLCAF.so
%attr(755,root,root) %{_libdir}/libTKMath.so
%attr(755,root,root) %{_libdir}/libTKMesh.so
%attr(755,root,root) %{_libdir}/libTKMeshVS.so
%attr(755,root,root) %{_libdir}/libTKOffset.so
%attr(755,root,root) %{_libdir}/libTKOpenGl.so
%attr(755,root,root) %{_libdir}/libTKOpenGlTest.so
%attr(755,root,root) %{_libdir}/libTKPrim.so
%attr(755,root,root) %{_libdir}/libTKQADraw.so
%attr(755,root,root) %{_libdir}/libTKRWMesh.so
%attr(755,root,root) %{_libdir}/libTKService.so
%attr(755,root,root) %{_libdir}/libTKShHealing.so
%attr(755,root,root) %{_libdir}/libTKStd.so
%attr(755,root,root) %{_libdir}/libTKStdL.so
%attr(755,root,root) %{_libdir}/libTKTObj.so
%attr(755,root,root) %{_libdir}/libTKTObjDRAW.so
%attr(755,root,root) %{_libdir}/libTKTopAlgo.so
%attr(755,root,root) %{_libdir}/libTKTopTest.so
%attr(755,root,root) %{_libdir}/libTKV3d.so
%attr(755,root,root) %{_libdir}/libTKVCAF.so
%attr(755,root,root) %{_libdir}/libTKViewerTest.so
%attr(755,root,root) %{_libdir}/libTKXCAF.so
%attr(755,root,root) %{_libdir}/libTKXDEDRAW.so
%attr(755,root,root) %{_libdir}/libTKXMesh.so
%attr(755,root,root) %{_libdir}/libTKXSBase.so
%attr(755,root,root) %{_libdir}/libTKXSDRAW.so
%attr(755,root,root) %{_libdir}/libTKXSDRAWDE.so
%attr(755,root,root) %{_libdir}/libTKXSDRAWGLTF.so
%attr(755,root,root) %{_libdir}/libTKXSDRAWIGES.so
%attr(755,root,root) %{_libdir}/libTKXSDRAWOBJ.so
%attr(755,root,root) %{_libdir}/libTKXSDRAWPLY.so
%attr(755,root,root) %{_libdir}/libTKXSDRAWSTEP.so
%attr(755,root,root) %{_libdir}/libTKXSDRAWSTL.so
%attr(755,root,root) %{_libdir}/libTKXSDRAWVRML.so
%attr(755,root,root) %{_libdir}/libTKXml.so
%attr(755,root,root) %{_libdir}/libTKXmlL.so
%attr(755,root,root) %{_libdir}/libTKXmlTObj.so
%attr(755,root,root) %{_libdir}/libTKXmlXCAF.so
%attr(755,root,root) %{_libdir}/libTKernel.so
%dir %{_includedir}/opencascade
%{_includedir}/opencascade/*.gxx
%{_includedir}/opencascade/*.h
%{_includedir}/opencascade/*.hxx
%{_includedir}/opencascade/*.lxx
%if %{with vtk}
%exclude %{_includedir}/opencascade/IVtk*.hxx
%endif
%{_libdir}/cmake/opencascade
%{_datadir}/opencascade/samples

%files inspector
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/TInspectorEXE
%attr(755,root,root) %{_bindir}/inspector.sh

%files inspector-libs
%defattr(644,root,root,755)
# R: libTKBRep libTKBin libTKBinL libTKBinXCAF libTKCAF libTKDESTEP libTKG3d libTKLCAF libTKMath libTKService libTKStd libTKStdL libTKTInspectorAPI libTKTreeModel libTKV3d libTKVCAF libTKView libTKXCAF libTKXml libTKXmlL libTKXmlXCAF libTKernel Qt5Core Qt5Gui Qt5Widgets
%attr(755,root,root) %{_libdir}/libTKDFBrowser.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKDFBrowser.so.7.8
# R: libTKBRep libTKMath libTKTInspectorAPI libTKTreeModel libTKernel Qt5Core Qt5Gui Qt5Widgets
%attr(755,root,root) %{_libdir}/libTKMessageModel.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKMessageModel.so.7.8
# R: libTKBRep libTKMath libTKMessageModel libTKService libTKTInspectorAPI libTKTopAlgo libTKTreeModel libTKV3d.so libTKView.so libTKernel QtCore QtWidgets
%attr(755,root,root) %{_libdir}/libTKMessageView.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKMessageView.so.7.8
# R: libTKBRep libTKG3d libTKMath libTKTInspecorAPI libTKTreeModel libTKV3d libTKView libTKernel Qt5Core Qt5Gui Qt5Widgets
%attr(755,root,root) %{_libdir}/libTKShapeView.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKShapeView.so.7.8
# R: libTKTInspectorAPI libTKTreeModel libTKernel Qt5Core Qt5Gui Qt5Widgets Qt5Xml
%attr(755,root,root) %{_libdir}/libTKTInspector.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKTInspector.so.7.8
# R: libTKBRep libTKG3d libTKMath libTKPrim libTKTopAlgo libTKV3d libTKernel Qt5Core
%attr(755,root,root) %{_libdir}/libTKTInspectorAPI.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKTInspectorAPI.so.7.8
# R: libTKCAF libTKDraw libTKTInspector liBTKTInspectorAPI libTKViewerTest libTKernel Qt5Core
%attr(755,root,root) %{_libdir}/libTKToolsDraw.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKToolsDraw.so.7.8
# R: libTKTInspectorAPI libTKernel Qt5Core Qt5Gui Qt5Widgets
%attr(755,root,root) %{_libdir}/libTKTreeModel.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKTreeModel.so.7.8
# R: libTKG3d libTKMath libTKService libTKTInspectorAPI libTKTreeModel libTKV3d libTKView libTKernel Qt5Core Qt5Gui Qt5Widgets
%attr(755,root,root) %{_libdir}/libTKVInspector.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKVInspector.so.7.8
# R: libTKBRep libTKG3d libTKMath libTKOpenGl libTKService libTKV3d libTKernel Qt5Core Qt5Gui Qt5Widgets
%attr(755,root,root) %{_libdir}/libTKView.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKView.so.7.8

%files inspector-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libTKDFBrowser.so
%attr(755,root,root) %{_libdir}/libTKMessageModel.so
%attr(755,root,root) %{_libdir}/libTKMessageView.so
%attr(755,root,root) %{_libdir}/libTKShapeView.so
%attr(755,root,root) %{_libdir}/libTKTInspector.so
%attr(755,root,root) %{_libdir}/libTKTInspectorAPI.so
%attr(755,root,root) %{_libdir}/libTKToolsDraw.so
%attr(755,root,root) %{_libdir}/libTKTreeModel.so
%attr(755,root,root) %{_libdir}/libTKVInspector.so
%attr(755,root,root) %{_libdir}/libTKView.so
%{_includedir}/opencascade/inspector

%if %{with vtk}
%files vtk
%defattr(644,root,root,755)
# R: libTKBRep libTKMath libTKService libTKTopAlgo libTKV3d libTKernel libvtkCommonCore libvtkCommonDataModel libvtkCommonExecutionModel libvtkCommonMath libvtkCommonTransforms libvtkFiltersGeneral libvtkInteractionStyle libvtkRenderingCore libvtkRenderingFreeType libvtkRenderingOpenGL2
%attr(755,root,root) %{_libdir}/libTKIVtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKIVtk.so.7.8
# R: libTKDraw libTKIVtk libTKMath libTKService libTKV3d libTKernel libX11 libvtkCommonCore libvtkCommonExecutionModel libvtkIOImage libvtkImagingCore libvtkInteractionStyle libvtkRenderingCore libvtkRenderingFreeType libvtkRenderingGL2PSOpenGL2 libvtkRenderingOpenGL2 tcl
%attr(755,root,root) %{_libdir}/libTKIVtkDraw.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libTKIVtkDraw.so.7.8

%files vtk-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libTKIVtk.so
%attr(755,root,root) %{_libdir}/libTKIVtkDraw.so
%{_includedir}/opencascade/IVtk*.hxx
%endif

%if %{with apidocs}
%files doc
%defattr(644,root,root,755)
%doc doc/{overview,refman}
%endif

%files samples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
