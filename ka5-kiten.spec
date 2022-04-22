#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	22.04.0
%define		kframever	5.56.0
%define		qtver		5.9.0
%define		kaname		kiten
Summary:	kiten
Name:		ka5-%{kaname}
Version:	22.04.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	http://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	ce82efa7952aa1d1896bcfe56658bf99
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= 5.11.1
BuildRequires:	Qt5Widgets-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= %{kframever}
BuildRequires:	kf5-karchive-devel >= %{kframever}
BuildRequires:	kf5-kcompletion-devel >= %{kframever}
BuildRequires:	kf5-kconfig-devel >= %{kframever}
BuildRequires:	kf5-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf5-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf5-kcrash-devel >= %{kframever}
BuildRequires:	kf5-kdoctools-devel >= %{kframever}
BuildRequires:	kf5-khtml-devel >= %{kframever}
BuildRequires:	kf5-ki18n-devel >= %{kframever}
BuildRequires:	kf5-knotifications-devel >= %{kframever}
BuildRequires:	kf5-kxmlgui-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kiten is a Japanese reference/study tool.

%description -l pl.UTF-8
Kiten jest narzędziem do nauki japońskiego.

%package data
Summary:	Data files for %{kaname}
Summary(pl.UTF-8):	Dane dla %{kaname}
Group:		X11/Applications
BuildArch:	noarch

%description data
Data files for %{kaname}.

%description data -l pl.UTF-8
Dane dla %{kaname}.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
install -d build
cd build
%cmake \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kiten
%attr(755,root,root) %{_bindir}/kitengen
%attr(755,root,root) %{_bindir}/kitenkanjibrowser
%attr(755,root,root) %{_bindir}/kitenradselect
%ghost %{_libdir}/libkiten.so.5
%attr(755,root,root) %{_libdir}/libkiten.so.*.*.*

%files data -f %{kaname}.lang
%defattr(644,root,root,755)
%{_desktopdir}/org.kde.kiten.desktop
%{_desktopdir}/org.kde.kitenkanjibrowser.desktop
%{_desktopdir}/org.kde.kitenradselect.desktop
%{_datadir}/config.kcfg/kiten.kcfg
%dir %{_datadir}/fonts/kanjistrokeorders
%{_datadir}/fonts/kanjistrokeorders/KanjiStrokeOrders.ttf
%{_iconsdir}/hicolor/128x128/apps/kiten.png
%{_iconsdir}/hicolor/16x16/apps/kiten.png
%{_iconsdir}/hicolor/22x22/apps/kiten.png
%{_iconsdir}/hicolor/32x32/apps/kiten.png
%{_iconsdir}/hicolor/48x48/apps/kiten.png
%{_iconsdir}/hicolor/64x64/apps/kiten.png
%{_iconsdir}/hicolor/scalable/apps/kiten.svgz
%{_datadir}/kiten
%{_datadir}/kxmlgui5/kiten
%{_datadir}/kxmlgui5/kitenkanjibrowser
%{_datadir}/kxmlgui5/kitenradselect
%{_datadir}/metainfo/org.kde.kiten.appdata.xml

%files devel
%defattr(644,root,root,755)
%{_includedir}/libkiten
%{_libdir}/libkiten.so
