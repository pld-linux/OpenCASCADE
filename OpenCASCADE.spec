#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# TODO:
# - separate libs-x (80% of libraries), follow Fedora split or split packages as suggested by Jason Kraftcheck in Debian
# - fix cmake hardocing dependencies on exact tbb soname

# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	draco		# Draco compression support
%bcond_with	ffmpeg		# FFmpeg support, needs ffmpeg < 5
%bcond_without	freeimage	# FreeImage support
%bcond_without	openvr		# OpenVR support
%bcond_without	qt		# Qt based inspector
%bcond_without	tbb		# TBB support
%bcond_without	vtk		# VTK toolkit

%{?use_default_jdk}

Summary:	OpenCASCADE CAE platform
Summary(pl.UTF-8):	Platforma CAE OpenCASCADE
Name:		OpenCASCADE
Version:	7.9.3
%define	tagver	%(echo %{version} | tr . _)
Release:	1
License:	LGPL v2.1 with Open CASCADE Exception v1.0
Group:		Applications/Engineering
#Source0Download https://dev.opencascade.org/release
Source0:	https://github.com/Open-Cascade-SAS/OCCT/archive/V%{tagver}/OCCT-%{tagver}.tar.gz
# Source0-md5:	724d6ad98f138b9cda7576679b8bff94
Patch1:		%{name}-inspector-data.patch
Patch4:		%{name}-X.patch
Patch5:		cmake-libdir.patch
URL:		https://www.opencascade.com/open-cascade-technology/
# FreeImagePlus library
%{?with_freeimage:BuildRequires:	FreeImage-devel}
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	bison >= 3.7.4
BuildRequires:	cmake >= 3.10
BuildRequires:	doxygen >= 1:1.8.4
%{?with_draco:BuildRequires:	draco-devel}
BuildRequires:	eigen3
# avcodec avformat avutil swscale
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel}
BuildRequires:	flex >= 2.6.4
BuildRequires:	freetype-devel >= 2
%ifnarch i386 i486
%buildrequires_jdk
%endif
BuildRequires:	libstdc++-devel >= 6:7
%{?with_openvr:BuildRequires:	openvr-devel}
BuildRequires:	rapidjson-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
%{?with_tbb:BuildRequires:	tbb-devel >= 2021.5}
BuildRequires:	tcl-devel >= 8.6
BuildRequires:	tk-devel >= 8.6
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
%{?with_tbb:%requires_eq tbb}
Requires:	%{name}-libs = %{version}-%{release}
%{?with_tbb:Requires:	tbb >= 2021.5}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abiver			7.9

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
Requires:	libstdc++-devel >= 6:7
# for CommandWindow.h
Requires:	tcl-devel
%{?with_tbb:%requires_eq tbb-devel}

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
%patch -P 1 -p1
%patch -P 4 -p1
%patch -P 5 -p1

%{__sed} -i -e '/set (CMAKE_CONFIGURATION_TYPES/ { s/INTERNAL/STRING/;s/ FORCE// }' CMakeLists.txt

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
bash adm/gendoc -overview -html
bash adm/gendoc -refman -html
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
%doc OCCT_LGPL_EXCEPTION.txt README.md
# R: libTKBRep libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKPrim libTKShHealing libTKTopAlgo libTKernel
%{_libdir}/libTKBO.so.*.*.*
%ghost %{_libdir}/libTKBO.so.%{abiver}
# R: libTKG2d libTKG3d libTKGeomBase libTKMath libTKernel
%{_libdir}/libTKBRep.so.*.*.*
%ghost %{_libdir}/libTKBRep.so.%{abiver}
# R: libTKBRep libTKBinL libTKCAF libTKCDF libTKLCAF libTKMath libTKernel
%{_libdir}/libTKBin.so.*.*.*
%ghost %{_libdir}/libTKBin.so.%{abiver}
# R: libTKCDF libTKLCAF libTKernel
%{_libdir}/libTKBinL.so.*.*.*
%ghost %{_libdir}/libTKBinL.so.%{abiver}
# R: libTKBinL libTKCDF libTKLCAF libTKTObj libTKernel
%{_libdir}/libTKBinTObj.so.*.*.*
%ghost %{_libdir}/libTKBinTObj.so.%{abiver}
# R: libTKBRep libTKBin libTKBinL libTKCAF libTKCDF libTKLCAF libTKMath libTKService libTKXCAF libTKernel
%{_libdir}/libTKBinXCAF.so.*.*.*
%ghost %{_libdir}/libTKBinXCAF.so.%{abiver}
# R: libTKBO libTKBRep libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKPrim libTKShHealing libTKTopAlgo libTKernel
%{_libdir}/libTKBool.so.*.*.*
%ghost %{_libdir}/libTKBool.so.%{abiver}
# R: libGKBO libTKBRep libTKCDF libTKG3d libTKGeomBase libTKLCAF libTKMath libTKTopAlgo libTKernel
%{_libdir}/libTKCAF.so.*.*.*
%ghost %{_libdir}/libTKCAF.so.%{abiver}
# R: libTKernel
%{_libdir}/libTKCDF.so.*.*.*
%ghost %{_libdir}/libTKCDF.so.%{abiver}
# R: libTKBO libTKBRep libTKBin libTKBinL libTKBool libTKCAF libTKCDF libTKDraw libTKFillet libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKLCAF libTKMath libTKPrim libTKStd libTKStdL libTKTopAlgo libTKV3d libTKVCAF libTKViewerTest libTKXml libTKXmlL libTKernel
%{_libdir}/libTKDCAF.so.*.*.*
%ghost %{_libdir}/libTKDCAF.so.%{abiver}
# R: libTKernel
%{_libdir}/libTKDE.so.*.*.*
%ghost %{_libdir}/libTKDE.so.%{abiver}
# R: libTKBRep libTKBin libTKBinL libTKBinTObj libTKBinXCAF libTKCDF libTKDE libTKLCAF libTKMath libTKStd libTKStdL libTKXCAF libTKXml libTKXmlL libTKXmlTObj libTKXmlTObj libTKXmlXCAF libTKernel
%{_libdir}/libTKDECascade.so.*.*.*
%ghost %{_libdir}/libTKDECascade.so.%{abiver}
# R: libTKBRep libTKDE libTKG3d libTKLCAF libTKMath libTKRWMesh libTKService libTKXCAF libTKernel
%{_libdir}/libTKDEGLTF.so.*.*.*
%ghost %{_libdir}/libTKDEGLTF.so.%{abiver}
# R: libTKBRep libTKBool libTKDE libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKLCAF libTKMath libTKPrim libTKShHealing libTKTopAlgo libTKXCAF libTKXSBase libTKernel %{?with_draco:draco}
%{_libdir}/libTKDEIGES.so.*.*.*
%ghost %{_libdir}/libTKDEIGES.so.%{abiver}
# R: libTKBRep libTKDE libTKG3d libTKLCAF libTKMath libTKMesh libTKRWMesh libTKService libTKXCAF libTKernel
%{_libdir}/libTKDEOBJ.so.*.*.*
%ghost %{_libdir}/libTKDEOBJ.so.%{abiver}
# R: libTKBRep libTKDE libTKG3d libTKLCAF libTKMath libTKRWMesh libTKXCAF libTKernel
%{_libdir}/libTKDEPLY.so.*.*.*
%ghost %{_libdir}/libTKDEPLY.so.%{abiver}
# R: libTKBRep libTKDE libTKG2d libTKG3d libTKGeomBase libTKLCAF libTKMath libTKShHealing libTKTopAlgo libTKXCAF libTKXSBase libTKernel
%{_libdir}/libTKDESTEP.so.*.*.*
%ghost %{_libdir}/libTKDESTEP.so.%{abiver}
# R: libTKBRep libTKDE libTKLCAF libTKMath libTKTopAlgo libTKXCAF libTKernel
%{_libdir}/libTKDESTL.so.*.*.*
%ghost %{_libdir}/libTKDESTL.so.%{abiver}
# R: libTKBRep libTKDE libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKHLR libTKLCAF libTKMath libTKMesh libTKPrim libTKRWMesh libTKTopAlgo libTKV3d libTKXCAF libTKernel
%{_libdir}/libTKDEVRML.so.*.*.*
%ghost %{_libdir}/libTKDEVRML.so.%{abiver}
# R: libTKBRep libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKHLR libTKMath libTKMesh libTKService libTKTopAlgo libTKernel libX11 tcl tk
%{_libdir}/libTKDraw.so.*.*.*
%ghost %{_libdir}/libTKDraw.so.%{abiver}
# R: libTKernel
%{_libdir}/libTKExpress.so.*.*.*
%ghost %{_libdir}/libTKExpress.so.%{abiver}
# R: libTKBO libTKBRep libTKBool libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKPrim libTKShHealing libTKTopAlgo libTKernel
%{_libdir}/libTKFeat.so.*.*.*
%ghost %{_libdir}/libTKFeat.so.%{abiver}
# R: libTKBO libTKBRep libTKBool libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKShHealing libTKTopAlgo libTKernel
%{_libdir}/libTKFillet.so.*.*.*
%ghost %{_libdir}/libTKFillet.so.%{abiver}
# R: libTKMath libTKernel
%{_libdir}/libTKG2d.so.*.*.*
%ghost %{_libdir}/libTKG2d.so.%{abiver}
# R: libTKG2d libTKMath libTKernel
%{_libdir}/libTKG3d.so.*.*.*
%ghost %{_libdir}/libTKG3d.so.%{abiver}
# R: libTKBRep libTKG2d libTKG3d libTKGeomBase libTKMath libTKernel
%{_libdir}/libTKGeomAlgo.so.*.*.*
%ghost %{_libdir}/libTKGeomAlgo.so.%{abiver}
# R: libTKG2d libTKG3d libTKMath libTKernel
%{_libdir}/libTKGeomBase.so.*.*.*
%ghost %{_libdir}/libTKGeomBase.so.%{abiver}
# R: libTKBRep libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKTopAlgo libTKernel
%{_libdir}/libTKHLR.so.*.*.*
%ghost %{_libdir}/libTKHLR.so.%{abiver}
# R: libTKCDF libTKernel
%{_libdir}/libTKLCAF.so.*.*.*
%ghost %{_libdir}/libTKLCAF.so.%{abiver}
# R: libTKernel
%{_libdir}/libTKMath.so.*.*.*
%ghost %{_libdir}/libTKMath.so.%{abiver}
# R: libTKBrep libTKG2d libTKG3d libTKGeomBase libTKMath libTKShHealing libTKTopAlgo libTKernel
%{_libdir}/libTKMesh.so.*.*.*
%ghost %{_libdir}/libTKMesh.so.%{abiver}
# R: libTKMath libTKService libTKV3d libTKernel
%{_libdir}/libTKMeshVS.so.*.*.*
%ghost %{_libdir}/libTKMeshVS.so.%{abiver}
# R: libTKBO libTKBRep libTKBool libTKFillet libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKPrim libTKShHealing libTKTopAlgo libTKernel
%{_libdir}/libTKOffset.so.*.*.*
%ghost %{_libdir}/libTKOffset.so.%{abiver}
# R: libTKMath libTKService libTKernel libGL libX11
%{_libdir}/libTKOpenGl.so.*.*.*
%ghost %{_libdir}/libTKOpenGl.so.%{abiver}
# R: libTKDraw libTKOpenGl libTKService libTKV3d libTKViewerTest libTKernel
%{_libdir}/libTKOpenGlTest.so.*.*.*
%ghost %{_libdir}/libTKOpenGlTest.so.%{abiver}
# R: libTKBRep libTKG2d libTKG3d libTKGeomBase libTKMath libTKTopAlgo libTKernel
%{_libdir}/libTKPrim.so.*.*.*
%ghost %{_libdir}/libTKPrim.so.%{abiver}
# R: libTKBO libTKBRep libTKBin libTKBinL libTKBinXCAF libTKBool libTKCAF libTKCDF libTKDCAF libTKDEIGES libTKDESTEP libTKDraw libTKFeat libTKFillet libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKHLR libTKLCAF libTKMath libTKMesh libTKOffset libTKPrim libTKService libTKShHealing libTKStd libTKStdL libTKTObj libTKTopAlgo libTKV3d libTKVCAF libTKViewerTest libTKXCAF libTKXSBase libTKXml libTKXmlL libTKernel %{?with_tbb:tbb}
%{_libdir}/libTKQADraw.so.*.*.*
%ghost %{_libdir}/libTKQADraw.so.%{abiver}
# R: libTKBRep libTKG3d liBTKLCAF libTKMath libTKService libTKXCAF libTKernel
%{_libdir}/libTKRWMesh.so.*.*.*
%ghost %{_libdir}/libTKRWMesh.so.%{abiver}
# R: libTKMath libTKernel libX11 fontconfig freetype %{?with_freeimage:FreeImage} %{?with_ffmpeg:ffmpeg-libs} %{?with_openvr:openvr}
%{_libdir}/libTKService.so.*.*.*
%ghost %{_libdir}/libTKService.so.%{abiver}
# R: libTKBrep libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKTopAlgo libTKernel
%{_libdir}/libTKShHealing.so.*.*.*
%ghost %{_libdir}/libTKShHealing.so.%{abiver}
# R: libTKBRep libTKCAF libTKCDF libTKG2d libG3d libGKLCAF libTKMath libTKStdL libTKernel
%{_libdir}/libTKStd.so.*.*.*
%ghost %{_libdir}/libTKStd.so.%{abiver}
# R: libTKCDF libTKLCAF libTKernel
%{_libdir}/libTKStdL.so.*.*.*
%ghost %{_libdir}/libTKStdL.so.%{abiver}
# R: libTKCDF libTKLCAF libTKernel
%{_libdir}/libTKTObj.so.*.*.*
%ghost %{_libdir}/libTKTObj.so.%{abiver}
# R: libTKBinTObj libTKDCAF libTKDraw libTKLCAF libTKTObj libTKXmlTObj libTKernel
%{_libdir}/libTKTObjDRAW.so.*.*.*
%ghost %{_libdir}/libTKTObjDRAW.so.%{abiver}
# R: libTKBRep libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKMath libTKernel
%{_libdir}/libTKTopAlgo.so.*.*.*
%ghost %{_libdir}/libTKTopAlgo.so.%{abiver}
# R: libTKBO libTKBRep libTKBool libTKDraw libTKFeat libTKFillet libTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKHLR libTKMath libTKMesh libTKOffset libTKPrim libTKShHealing libTKTopAlgo libTKV3d libTKernel
%{_libdir}/libTKTopTest.so.*.*.*
%ghost %{_libdir}/libTKTopTest.so.%{abiver}
# R: libTKBRep liBTKG2d libTKG3d libTKGeomAlgo libTKGeomBase libTKHLR libTKMath libTKMesh libTKService libTKTopAlgo libTKernel
%{_libdir}/libTKV3d.so.*.*.*
%ghost %{_libdir}/libTKV3d.so.%{abiver}
# R: libTKBRep libTKCAF libTKG3d libTKGeomBase libTKLCAF libTKMath libTKService libTKTopAlgo libTKV3d libTKernel
%{_libdir}/libTKVCAF.so.*.*.*
%ghost %{_libdir}/libTKVCAF.so.%{abiver}
# R: libTKBRep libTKDraw libTKFillet libTKG3d libTKGeomAlgo libTKGeomBase libTKHLR libTKMath libTKService libTKTopAlgo libTKV3d libTKernel libX11 tcl
%{_libdir}/libTKViewerTest.so.*.*.*
%ghost %{_libdir}/libTKViewerTest.so.%{abiver}
# R: libTKBRep libTKCAF libTKCDF libTKG3d libTKLCAF libTKMath libTKService libTKTopAlgo libTKV3d libTKVCAF libTKernel
%{_libdir}/libTKXCAF.so.*.*.*
%ghost %{_libdir}/libTKXCAF.so.%{abiver}
# R: libTKBRep libTKBinXCAF libTKCAF libTKCDF libTKDCAF libTKDESTEP libTKDraw libTKG3d libTKLCAF libTKMath libTKMesh libTKService libTKTopAlgo libTKV3d libTKVCAF libTKViewerTest libTKXCAF libTKXSBase libTKXSDRAW libTKXmlXCAF libTKernel
%{_libdir}/libTKXDEDRAW.so.*.*.*
%ghost %{_libdir}/libTKXDEDRAW.so.%{abiver}
# R: libTKMath libTKMesh libTKernel
%{_libdir}/libTKXMesh.so.*.*.*
%ghost %{_libdir}/libTKXMesh.so.%{abiver}
# R: libTKBRep libTKG2d libTKG3d libTKMath libTKShHealing libTKTopAlgo libTKernel
%{_libdir}/libTKXSBase.so.*.*.*
%ghost %{_libdir}/libTKXSBase.so.%{abiver}
# R: libTKDraw libTKG2d libTKG3d libTKXCAF libTKXSBase libTKernel
%{_libdir}/libTKXSDRAW.so.*.*.*
%ghost %{_libdir}/libTKXSDRAW.so.%{abiver}
# R: libTKDCAF libTKDE libTKDECascade libTKDraw.so libTKLCAF libTKMath libTKXSDRAW libTKernel
%{_libdir}/libTKXSDRAWDE.so.*.*.*
%ghost %{_libdir}/libTKXSDRAWDE.so.%{abiver}
# R: libTKDCAF libTKDEGLTF libTKDraw.so libTKLCAF libTKMath libTKRWMesh libTKXCAF libTKXSDRAW libTKernel
%{_libdir}/libTKXSDRAWGLTF.so.*.*.*
%ghost %{_libdir}/libTKXSDRAWGLTF.so.%{abiver}
# R: libTKBRep libTKDCAF libTKDEIGES libTKDraw libTKLCAF libTKXSBase libTKXSDRAW libTKernel
%{_libdir}/libTKXSDRAWIGES.so.*.*.*
%ghost %{_libdir}/libTKXSDRAWIGES.so.%{abiver}
# R: libTKBRep libTKDCAF libTKDEOBJ libTKDraw libTKLCAF libTKMath libTKRWMesh libTKXCAF libTKXSDRAW libTKernel
%{_libdir}/libTKXSDRAWOBJ.so.*.*.*
%ghost %{_libdir}/libTKXSDRAWOBJ.so.%{abiver}
# R: libTKBRep libTKDCAF libTKDEPLY libTKDraw libTKG3d libTKLCAF libTKMath libTKRWMesh libTKTopAlgo libTKXCAF libTKXSDRAW libTKernel
%{_libdir}/libTKXSDRAWPLY.so.*.*.*
%ghost %{_libdir}/libTKXSDRAWPLY.so.%{abiver}
# R: libTKDCAF libTKDESTEP libTKDraw libTKLCAF libTKMath libTKXSBase libTKXSDRAW libTKernel
%{_libdir}/libTKXSDRAWSTEP.so.*.*.*
%ghost %{_libdir}/libTKXSDRAWSTEP.so.%{abiver}
# R: libTKBRep libTKDESTL libTKDraw libTKMath libTKMeshVS libTKService libTKV3d libTKViewerTest libTKXSDRAW libTKernel
%{_libdir}/libTKXSDRAWSTL.so.*.*.*
%ghost %{_libdir}/libTKXSDRAWSTL.so.%{abiver}
# R: libTKDCAF libTKDEVRML libTKDraw libTKLCAF libTKMath libTKRWMesh libTKXCAF libTKXSBase libTKXSDRAW libTKernel
%{_libdir}/libTKXSDRAWVRML.so.*.*.*
%ghost %{_libdir}/libTKXSDRAWVRML.so.%{abiver}
# R: libTKBRep libTKCAF libTKCDF libTKLCAF libTKMath libTKXmlL libTKernel
%{_libdir}/libTKXml.so.*.*.*
%ghost %{_libdir}/libTKXml.so.%{abiver}
# R: libTKCDF libTKLCAF libTKMath libTKernel
%{_libdir}/libTKXmlL.so.*.*.*
%ghost %{_libdir}/libTKXmlL.so.%{abiver}
# R: R: libTKCDF libTKLCAF libTKTObj libTKXmlL libTKernel
%{_libdir}/libTKXmlTObj.so.*.*.*
%ghost %{_libdir}/libTKXmlTObj.so.%{abiver}
# R: libTKBRep libTKCAF libTKCDF libTKLCAF libTKMath libTKService libTKXCAF libTKXml libTKXmlL libTKernel
%{_libdir}/libTKXmlXCAF.so.*.*.*
%ghost %{_libdir}/libTKXmlXCAF.so.%{abiver}
# R: (libstdc++) %{?with_tbb:tbb}
%{_libdir}/libTKernel.so.*.*.*
%ghost %{_libdir}/libTKernel.so.%{abiver}
%dir %{_libdir}/opencascade
%{_libdir}/opencascade/custom*.sh
%{_libdir}/opencascade/env.sh

%files devel
%defattr(644,root,root,755)
%{_libdir}/libTKBO.so
%{_libdir}/libTKBRep.so
%{_libdir}/libTKBin.so
%{_libdir}/libTKBinL.so
%{_libdir}/libTKBinTObj.so
%{_libdir}/libTKBinXCAF.so
%{_libdir}/libTKBool.so
%{_libdir}/libTKCAF.so
%{_libdir}/libTKCDF.so
%{_libdir}/libTKDCAF.so
%{_libdir}/libTKDE.so
%{_libdir}/libTKDECascade.so
%{_libdir}/libTKDEGLTF.so
%{_libdir}/libTKDEIGES.so
%{_libdir}/libTKDEOBJ.so
%{_libdir}/libTKDEPLY.so
%{_libdir}/libTKDESTEP.so
%{_libdir}/libTKDESTL.so
%{_libdir}/libTKDEVRML.so
%{_libdir}/libTKDraw.so
%{_libdir}/libTKExpress.so
%{_libdir}/libTKFeat.so
%{_libdir}/libTKFillet.so
%{_libdir}/libTKG2d.so
%{_libdir}/libTKG3d.so
%{_libdir}/libTKGeomAlgo.so
%{_libdir}/libTKGeomBase.so
%{_libdir}/libTKHLR.so
%{_libdir}/libTKLCAF.so
%{_libdir}/libTKMath.so
%{_libdir}/libTKMesh.so
%{_libdir}/libTKMeshVS.so
%{_libdir}/libTKOffset.so
%{_libdir}/libTKOpenGl.so
%{_libdir}/libTKOpenGlTest.so
%{_libdir}/libTKPrim.so
%{_libdir}/libTKQADraw.so
%{_libdir}/libTKRWMesh.so
%{_libdir}/libTKService.so
%{_libdir}/libTKShHealing.so
%{_libdir}/libTKStd.so
%{_libdir}/libTKStdL.so
%{_libdir}/libTKTObj.so
%{_libdir}/libTKTObjDRAW.so
%{_libdir}/libTKTopAlgo.so
%{_libdir}/libTKTopTest.so
%{_libdir}/libTKV3d.so
%{_libdir}/libTKVCAF.so
%{_libdir}/libTKViewerTest.so
%{_libdir}/libTKXCAF.so
%{_libdir}/libTKXDEDRAW.so
%{_libdir}/libTKXMesh.so
%{_libdir}/libTKXSBase.so
%{_libdir}/libTKXSDRAW.so
%{_libdir}/libTKXSDRAWDE.so
%{_libdir}/libTKXSDRAWGLTF.so
%{_libdir}/libTKXSDRAWIGES.so
%{_libdir}/libTKXSDRAWOBJ.so
%{_libdir}/libTKXSDRAWPLY.so
%{_libdir}/libTKXSDRAWSTEP.so
%{_libdir}/libTKXSDRAWSTL.so
%{_libdir}/libTKXSDRAWVRML.so
%{_libdir}/libTKXml.so
%{_libdir}/libTKXmlL.so
%{_libdir}/libTKXmlTObj.so
%{_libdir}/libTKXmlXCAF.so
%{_libdir}/libTKernel.so
%dir %{_includedir}/opencascade
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
%{_libdir}/libTKDFBrowser.so.*.*.*
%ghost %{_libdir}/libTKDFBrowser.so.%{abiver}
# R: libTKBRep libTKMath libTKTInspectorAPI libTKTreeModel libTKernel Qt5Core Qt5Gui Qt5Widgets
%{_libdir}/libTKMessageModel.so.*.*.*
%ghost %{_libdir}/libTKMessageModel.so.%{abiver}
# R: libTKBRep libTKMath libTKMessageModel libTKService libTKTInspectorAPI libTKTopAlgo libTKTreeModel libTKV3d.so libTKView.so libTKernel QtCore QtWidgets
%{_libdir}/libTKMessageView.so.*.*.*
%ghost %{_libdir}/libTKMessageView.so.%{abiver}
# R: libTKBRep libTKG3d libTKMath libTKTInspecorAPI libTKTreeModel libTKV3d libTKView libTKernel Qt5Core Qt5Gui Qt5Widgets
%{_libdir}/libTKShapeView.so.*.*.*
%ghost %{_libdir}/libTKShapeView.so.%{abiver}
# R: libTKTInspectorAPI libTKTreeModel libTKernel Qt5Core Qt5Gui Qt5Widgets Qt5Xml
%{_libdir}/libTKTInspector.so.*.*.*
%ghost %{_libdir}/libTKTInspector.so.%{abiver}
# R: libTKBRep libTKG3d libTKMath libTKPrim libTKTopAlgo libTKV3d libTKernel Qt5Core
%{_libdir}/libTKTInspectorAPI.so.*.*.*
%ghost %{_libdir}/libTKTInspectorAPI.so.%{abiver}
# R: libTKCAF libTKDraw libTKTInspector liBTKTInspectorAPI libTKViewerTest libTKernel Qt5Core
%{_libdir}/libTKToolsDraw.so.*.*.*
%ghost %{_libdir}/libTKToolsDraw.so.%{abiver}
# R: libTKTInspectorAPI libTKernel Qt5Core Qt5Gui Qt5Widgets
%{_libdir}/libTKTreeModel.so.*.*.*
%ghost %{_libdir}/libTKTreeModel.so.%{abiver}
# R: libTKG3d libTKMath libTKService libTKTInspectorAPI libTKTreeModel libTKV3d libTKView libTKernel Qt5Core Qt5Gui Qt5Widgets
%{_libdir}/libTKVInspector.so.*.*.*
%ghost %{_libdir}/libTKVInspector.so.%{abiver}
# R: libTKBRep libTKG3d libTKMath libTKOpenGl libTKService libTKV3d libTKernel Qt5Core Qt5Gui Qt5Widgets
%{_libdir}/libTKView.so.*.*.*
%ghost %{_libdir}/libTKView.so.%{abiver}

%files inspector-devel
%defattr(644,root,root,755)
%{_libdir}/libTKDFBrowser.so
%{_libdir}/libTKMessageModel.so
%{_libdir}/libTKMessageView.so
%{_libdir}/libTKShapeView.so
%{_libdir}/libTKTInspector.so
%{_libdir}/libTKTInspectorAPI.so
%{_libdir}/libTKToolsDraw.so
%{_libdir}/libTKTreeModel.so
%{_libdir}/libTKVInspector.so
%{_libdir}/libTKView.so
%{_includedir}/opencascade/inspector

%if %{with vtk}
%files vtk
%defattr(644,root,root,755)
# R: libTKBRep libTKMath libTKService libTKTopAlgo libTKV3d libTKernel libvtkCommonCore libvtkCommonDataModel libvtkCommonExecutionModel libvtkCommonMath libvtkCommonTransforms libvtkFiltersGeneral libvtkInteractionStyle libvtkRenderingCore libvtkRenderingFreeType libvtkRenderingOpenGL2
%{_libdir}/libTKIVtk.so.*.*.*
%ghost %{_libdir}/libTKIVtk.so.%{abiver}
# R: libTKDraw libTKIVtk libTKMath libTKService libTKV3d libTKernel libX11 libvtkCommonCore libvtkCommonExecutionModel libvtkIOImage libvtkImagingCore libvtkInteractionStyle libvtkRenderingCore libvtkRenderingFreeType libvtkRenderingGL2PSOpenGL2 libvtkRenderingOpenGL2 tcl
%{_libdir}/libTKIVtkDraw.so.*.*.*
%ghost %{_libdir}/libTKIVtkDraw.so.%{abiver}

%files vtk-devel
%defattr(644,root,root,755)
%{_libdir}/libTKIVtk.so
%{_libdir}/libTKIVtkDraw.so
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
