Name:           gnome-initial-setup
Version:        3.18.0
Release:        1%{?dist}
Summary:        Bootstrapping your OS

License:        GPLv2+
URL:            https://live.gnome.org/GnomeOS/Design/Whiteboards/InitialSetup
Source0:        https://download.gnome.org/sources/%{name}/3.18/%{name}-%{version}.tar.xz
Patch10:	gnome-initial-setup-3.10.1.1-read-pretty_name.patch

%global nm_version 0.9.6.4
%global glib_required_version 2.36.0
%global gtk_required_version 3.11.3
%global geoclue_version 2.1.2

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
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(cheese)
BuildRequires:  pkgconfig(cheese-gtk) >= 3.3.5
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(geoclue-2.0) >= %{geoclue_version}
BuildRequires:  pkgconfig(gweather-3.0)
BuildRequires:  pkgconfig(goa-1.0)
BuildRequires:  pkgconfig(goa-backend-1.0)
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk_required_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib_required_version}
BuildRequires:  pkgconfig(gio-2.0) >= %{glib_required_version}
BuildRequires:  pkgconfig(gio-unix-2.0) >= %{glib_required_version}
BuildRequires:  pkgconfig(gdm)
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:  pkgconfig(webkit2gtk-4.0)
BuildRequires:  krb5-devel
BuildRequires:  ibus-devel
BuildRequires:  rest-devel
BuildRequires:  polkit-devel
BuildRequires:  libsecret-devel

# gnome-initial-setup is being run by gdm
Requires: gdm
Requires: geoclue2 >= %{geoclue_version}
# we install a rules file
Requires: polkit-js-engine
Requires: /usr/bin/gkbd-keyboard-display

Requires(pre): shadow-utils

Provides: user(%name)

%description
GNOME Initial Setup is an alternative to firstboot, providing
a good setup experience to welcome you to your system, and walks
you through configuring it. It is integrated with gdm.

%prep
%setup -q
%patch10 -p1 -b .read-pretty_name

%build
%configure
make %{?_smp_mflags}

%install
%make_install
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
%license COPYING
%doc README
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
* Tue Oct 20 2015 Arkady L. Shane <ashejn@russianfedora.pro> - 3.18.0-1.R
- read NAME from PRETTY_NAME var of os-release

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Mon Aug 31 2015 Kalev Lember <klember@redhat.com> - 3.17.91-1
- Update to 3.17.91

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90
- Use make_install macro

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 3.17.4-2
- Rebuilt for libcheese soname bump

* Mon Jul 27 2015 David King <amigadave@amigadave.com> - 3.17.4-1
- Update to 3.17.4

* Wed Jul 22 2015 David King <amigadave@amigadave.com> - 3.16.3-3
- Bump for new gnome-desktop3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Matthias Clasen <mclasen@redhat.com> - 3.16.3-1
- Update to 3.16.3

* Tue May 12 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-1
- Update to 3.16.2

* Wed Apr 15 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Wed Mar 18 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92

* Thu Mar 05 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91.1-1
- Update to 3.15.91.1

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-1
- Update to 3.15.91
- Use the %%license macro for the COPYING file

* Thu Feb 19 2015 Matthias Clasen <mclasen@redhat.com> - 3.15.90.1-1
- Update to 3.15.90.1

* Tue Dec 16 2014 Rui Matos <rmatos@redhat.com> - 3.14.2.1-2
- Resolves: rhbz#1172363

* Tue Nov 11 2014 Rui Matos <rmatos@redhat.com> - 3.14.2.1-1
- Update to 3.14.2.1

* Mon Nov 10 2014 Rui Matos <rmatos@redhat.com> - 3.14.2-1
- Update to 3.14.2
- Resolves: rhbz#1158442

* Fri Oct 31 2014 Rui Matos <rmatos@redhat.com> - 3.14.1-3
- Resolves: rhbz#1151519

* Tue Oct 21 2014 Rui Matos <rmatos@redhat.com> - 3.14.1-2
- Resolves: rhbz#1154206

* Sat Oct 11 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-1
- Update to 3.14.1

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Wed Sep 17 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.7-1
- Update to 3.13.7

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.6-1
- Update to 3.13.6

* Mon Sep 08 2014 Adam Williamson <awilliam@redhat.com> - 3.13.5-2
- backport upstream patch to offer full list of keyboard layouts (BGO #729208)

* Wed Sep 03 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.5-1
- Update to 3.13.5

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Matthias Clasen <mclasen@redhat.com> - 3.13.4-2
- Drop the yelp focus patch (we've dropped the yelp patch it depends on)

* Fri Jul 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-1
- Update to 3.13.4

* Thu Jul 24 2014 Matthias Clasen <mclasen@redhat.com> - 3.12.1-3
- Fix a memory corruption crash (#1116478)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1

* Tue Mar 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0-1
- Update to 3.12.0

* Thu Mar 20 2014 Richard Hughes <rhughes@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Sat Mar 08 2014 Richard Hughes <rhughes@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Fri Feb 28 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Wed Feb 19 2014 Kalev Lember <kalevlember@gmail.com> - 3.10.1.1-5
- Rebuilt for libgnome-desktop soname bump

* Fri Nov 29 2013 Rui Matos <rmatos@redhat.com> - 3.10.1.1-4
- Resolves: rhbz#1035548 - Disables the GOA page in new user mode

* Thu Nov 28 2013 Rui Matos <rmatos@redhat.com> - 3.10.1.1-3
- Resolves: rhbz#1027507 - [abrt] gnome-initial-setup-3.10.1.1-2.fc20: magazine_chain_pop_head

* Fri Nov  1 2013 Matthias Clasen <mclasen@redhat.com> - 3.10.1.1-2
- Fix goa add dialog to not be empty

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1.1-1
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
