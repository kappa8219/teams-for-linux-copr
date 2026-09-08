%global debug_package %{nil}
%global __strip /bin/true
%global __requires_exclude_from /opt/teams-for-linux/.*

Name:           teams-for-linux
Version:        2.20.0
Release:        1%{?dist}
Summary:        Unofficial Microsoft Teams client for Linux
License:        GPL-3.0-or-later
URL:            https://github.com/IsmaelMartinez/teams-for-linux
Source0:        https://github.com/IsmaelMartinez/teams-for-linux/releases/download/v%{version}/teams-for-linux-%{version}.x86_64.rpm
ExclusiveArch:  x86_64

BuildRequires:  cpio
BuildRequires:  desktop-file-utils
BuildRequires:  rpm

Requires:       alsa-lib
Requires:       at-spi2-core
Requires:       gtk3
Requires:       libnotify
Requires:       libXScrnSaver
Requires:       mesa-libgbm
Requires:       nss
Requires:       xdg-utils

%description
Teams for Linux is an unofficial Microsoft Teams client for Linux using
Electron. It wraps the Teams web application as a standalone desktop app.

%prep
echo "4b6899c3f4e339d3717e39dee3ea7ed0a0d2c95578fcc81ace7e38913a820761  %{SOURCE0}" | sha256sum --check

%install
rpm2cpio %{SOURCE0} | cpio --extract --make-directories --quiet --directory %{buildroot}
install -d %{buildroot}%{_bindir}
ln -s /opt/teams-for-linux/teams-for-linux %{buildroot}%{_bindir}/teams-for-linux

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/teams-for-linux.desktop

%files
%license /opt/teams-for-linux/LICENSE.electron.txt
%license /opt/teams-for-linux/LICENSES.chromium.html
/opt/teams-for-linux
%{_bindir}/teams-for-linux
%{_datadir}/applications/teams-for-linux.desktop
%{_datadir}/icons/hicolor/*/apps/teams-for-linux.png

%changelog
* Tue Sep 08 2026 OK <o.kraievyi@gmail.com> - 2.20.0-1
- Update to 2.20.0

* Thu Aug 27 2026 OK <o.kraievyi@gmail.com> - 2.18.1-1
- Update to 2.18.1

* Mon Aug 24 2026 OK <o.kraievyi@gmail.com> - 2.17.0-1
- Package the upstream Teams for Linux RPM for COPR
