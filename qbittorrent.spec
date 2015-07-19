%bcond_without nox
#debuginfo-without-sources
%define debug_package	%{nil}
%define gitdate %{nil}
Name:		qbittorrent
Version:	3.2.0
Summary:	A lightweight but featureful BitTorrent client
Group:		Networking/File transfer
License:	GPLv2+
Url:		http://qbittorrent.sourceforge.net/
%if "%gitdate" != ""
Source0:	qbittorrent-%{gitdate}.tar.gz
Release:	0.%{gitdate}.1
%else
Source0:	http://downloads.sourceforge.net/project/qbittorrent/qbittorrent/qbittorrent-%{version}/qbittorrent-%{version}.tar.xz
Release:	2
%endif
Patch0:		qbittorrent-3.2.0-compile.patch
BuildRequires:	qt5-devel
BuildRequires:	qt5-linguist-tools
BuildRequires:	qtchooser
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libtorrent-rasterbar)
Requires:	python
Requires:	geoip

%description
A lightweight but feature-full BitTorrent client that aims to be very easy 
to use. It is multi-platform and provides a Qt4 graphical interface.

%package -n %{name}-nox
Summary:	A Headless Bittorrent Client
Group:		Networking/File transfer

%description -n %{name}-nox
A Headless Bittorrent Client with a feature rich Web UI allowing users to
control the clinet remotely.

%prep
%if "%gitdate" != ""
%setup -q -n %{name}-%{gitdate}
%else
%setup -q
%endif
%patch0 -p1

%build
%setup_compile_flags

sed -i -e 's,@QBT_CONF_EXTRA_CFLAGS@,@QBT_CONF_EXTRA_CFLAGS@ -std=gnu++1y,' conf.pri.in

# headless aka nox
%if %{with nox}
%__mkdir build-nox
pushd build-nox
  ../configure	--prefix=%{_prefix} \
		--disable-gui \
		--disable-geoip-database \
		--with-qt5
  %__cp conf.pri ..
  %make
  %__mv -f ../conf.pri ../conf.pri.nox
popd
%endif

# GUI
mkdir build-gui
pushd build-gui
  ../configure	--prefix=%{_prefix} --with-qt5
  cp conf.pri ..
  %make 
  mv -f ../conf.pri ../conf.pri.gui
popd

%install
# install headless part
%if %{with nox}
cp -f conf.pri.nox conf.pri
pushd build-nox
  make INSTALL_ROOT=%{buildroot} install
popd
%endif

# install gui
cp -f conf.pri.gui conf.pri
pushd build-gui
  make INSTALL_ROOT=%{buildroot} install
popd

%files
%doc AUTHORS Changelog COPYING NEWS TODO
%{_bindir}/%{name}
%{_datadir}/applications/qBittorrent.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/qbittorrent.png
%{_datadir}/appdata/qBittorrent.appdata.xml
%{_mandir}/man1/%{name}.1*

%if %{with nox}
%files -n  %{name}-nox
%{_bindir}/%{name}-nox
%{_mandir}/man1/%{name}-nox.1*
%endif

