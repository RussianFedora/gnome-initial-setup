Name:           gnome-initial-setup
Version:        3.10.1.1
Release:        1%{?dist}
Summary:        Bootstrapping your OS

License:        GPLv2+
URL:            https://live.gnome.org/GnomeOS/Design/Whiteboards/InitialSetup
Source0:        http://download.gnome.org/sources/%{name}/3.10/%{name}-%{version}.tar.xz

# this depends on a yelp patch that hasn't been merged upstream yet
# https://bugzilla.gnome.org/show_bug.cgi?id=687957
Patch0: yelp-fixes.patch
# Read PRETTY_NAME istead of NAME for RFRemix
Patch1:		gnome-initial-setup-3.10.1.1-read-pretty_name.patch

%global nm_version 0.9.6.4
%global glib_required_version 2.36.0
%global gtk_required_version 3.7.11

BuildRequires:  krb5-devel
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  libpwquality-devel
BuildRequires:  pkgconfig(NetworkManager) >= %{nm_version}
BuildRequires:  pkgconfig(libnm-glib) >= %{nm_version}
BuildRequires:  pkgconfig(libnm-util) >= %{nm_version}
BuildRequires:  pkgconfig(libnm-gtk)
BuildRequires:  pkgconfig(accountsservice)
BuildRequires:  pkgconfig(gnome-desktop-3.0)
BuildRequires:  pkgconfig(gstreamer-0.10)
BuildRequires:  pkgconfig(cheese)
BuildRequires:  pkgconfig(cheese-gtk) >= 3.3.5
BuildRequires:  pkgconfig(geoclue)
BuildRequires:  pkgconfig(gweather-3.0)
BuildRequires:  pkgconfig(goa-1.0)
BuildRequires:  pkgconfig(goa-backend-1.0)
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk_required_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib_required_version}
BuildRequires:  pkgconfig(gio-2.0) >= %{glib_required_version}
BuildRequires:  pkgconfig(gio-unix-2.0) >= %{glib_required_version}
BuildRequires:  pkgconfig(gdm)
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:  krb5-devel
BuildRequires:  autoconf automake libtool
BuildRequires:  gnome-common
BuildRequires:  ibus-devel
BuildRequires:  polkit-devel

# gnome-initial-setup is being run by gdm
Requires: gdm
# we install a rules file
Requires: polkit-js-engine
Requires: /usr/bin/gkbd-keyboard-display

Requires(pre): shadow-utils

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

Provides: user(%name)

%description
GNOME Initial Setup is an alternative to firstboot, providing
a good setup experience to welcome you to your system, and walks
you through configuring it. It is integrated with gdm.

%prep
%setup -q
%patch0 -p1 -b .yelp-fixes
%patch1 -p1 -b .pretty_name

autoreconf -i -f

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Desktop file does not (and probably will not) ever validate, as it uses
# an absolute path /tmp/-style trigger to determine whether to autostart.
# desktop-file-validate %%{buildroot}/%%{_sysconfdir}/xdg/autostart/gnome-welcome-tour.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/gnome-initial-setup-copy-worker.desktop
desktop-file-validate %{buildroot}%{_datadir}/gdm/greeter/applications/gnome-initial-setup.desktop
desktop-file-validate %{buildroot}%{_datadir}/gdm/greeter/applications/setup-shell.desktop

mkdir -p %{buildroot}%{_localstatedir}/lib/gnome-initial-setup

%find_lang %{name}

%pre
useradd -rM -d /run/gnome-initial-setup/ -s /sbin/nologin %{name} &>/dev/null || :

%files -f %{name}.lang
%doc COPYING README
%{_libexecdir}/gnome-initial-setup
%{_libexecdir}/gnome-initial-setup-copy-worker
%{_libexecdir}/gnome-welcome-tour
%{_sysconfdir}/xdg/autostart/gnome-welcome-tour.desktop
%{_sysconfdir}/xdg/autostart/gnome-initial-setup-copy-worker.desktop
%{_sysconfdir}/xdg/autostart/gnome-initial-setup-first-login.desktop

%{_datadir}/gdm/greeter/applications/gnome-initial-setup.desktop
%{_datadir}/gdm/greeter/applications/setup-shell.desktop
%{_datadir}/gnome-session/sessions/gnome-initial-setup.session
%{_datadir}/gnome-shell/modes/initial-setup.json
%{_datadir}/polkit-1/rules.d/20-gnome-initial-setup.rules

%changelog
* Wed Oct 23 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 3.10.1.1-1.R
- read PRETTY_NAME instead of NAME from /etc/os-release

* Tue Oct 15 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1.1-1
- Update to 3.10.1.1

* Thu Sep 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0.1-1
- Update to 3.10.0.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 0.12-7
- Rebuilt for libgnome-desktop soname bump

* Fri Aug 23 2013 Kalev Lember <kalevlember@gmail.com> - 0.12-6
- Rebuilt for gnome-online-accounts soname bump

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 0.12-5
- Rebuilt for cogl 1.15.4 soname bump

* Tue Aug 06 2013 Adam Williamson <awilliam@redhat.com> - 0.12-4
- rebuild for new libgweather

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Kalev Lember <kalevlember@gmail.com> - 0.12-2
- Rebuilt for libgweather 3.9.3 soname bump

* Mon Jun 17 2013 Rui Matos <rmatos@redhat.com> - 0.12-1
- Update to 0.12

* Fri Jun  7 2013 Matthias Clasen <mclasen@redhat.com> - 0.11-2
- Require polkit-js-engine

* Tue May 28 2013 Matthias Clasen <mclasen@redhat.com> - 0.11-1
- Update to 0.11

* Tue May 14 2013 Rui Matos <rmatos@redhat.com> - 0.10-1
- Update to 0.10
- Add BuildRequires on polkit-devel
- Update files list

* Thu May  2 2013 Rui Matos <rmatos@redhat.com> - 0.9-2
- Remove unused patches
- Add build requires for ibus

* Tue Apr 16 2013 Matthias Clasen <mclasen@redhat.com> - 0.9-1
- Update to 0.9

* Tue Apr 16 2013 Ray Strode <rstrode@redhat.com> 0.8-4
- Add requires for keyboard viewer app

* Wed Mar 20 2013 Ray Strode <rstrode@redhat.com> 0.8-3
- Add cosimoc fix for gd page transitions

* Wed Mar 20 2013 Ray Strode <rstrode@redhat.com> 0.8-2
- Disable gd page transitions for now since they don't
  completely work right (ask adamw).
- Fix crasher when realmd goes away

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 0.8-1
- Update to 0.8

* Tue Mar 12 2013 Matthias Clasen <mclasen@redhat.com> - 0.7-1
- Update to 0.7

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 0.6-4
- Rebuilt for cogl soname bump

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.6-3
- Rebuilt for libgnome-desktop soname bump

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-2
- Rebuild for new cogl

* Wed Jan 16 2013 Matthias Clasen <mclasen@redhat.com> - 0.6-1
- 0.6

* Fri Jan 11 2013 Matthias Clasen <mclasen@redhat.com> - 0.5-1
- 0.5

* Fri Dec 21 2012 Kalev Lember <kalevlember@gmail.com> - 0.4-2
- Rebuilt for libgweather soname bump

* Thu Nov 22 2012 Matthias Clasen <mclasen@redhat.com> - 0.4-1
- 0.4

* Fri Oct 26 2012 Jasper St. Pierre <jstpierre@mecheye.net> - 0.3-3
- Add krb5

* Fri Oct 26 2012 Jasper St. Pierre <jstpierre@mecheye.net> - 0.3-2
- 0.3-2

* Thu Oct 18 2012 Matthias Clsaen <mclasen@redhat.com> - 0.3-1
- 0.3

* Fri Sep 14 2012 Matthias Clasen <mclasen@redhat.com> - 0.2-2
- Add Requires: gdm

* Wed Aug 29 2012 Jasper St. Pierre <jstpierre@mecheye.net> - 0.2-1
- Update to 0.2

* Fri Jun 08 2012 Jasper St. Pierre <jstpierre@mecheye.net> - 0.1
- Initial packaging.
