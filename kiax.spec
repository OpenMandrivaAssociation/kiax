%define svn	122
%define rel	3

%if %svn
%define release		%mkrel 0.%{svn}.2
%define distname	%{name}-%{svn}.tar.lzma
%define dirname		%{name}
%else
%define release		%mkrel %{rel}
%define distname	%{name}-%{version}.tar.lzma
%define dirname		%{name}-%{version}
%endif

Summary:	IAX client application (softphone)
Name:		kiax
Version:	2.1
Release:	%{release}
License:	GPL+ and LGPL+
Group:		Graphical desktop/KDE
URL:		http://kiax.org/
# They don't seem hot on source tarballs. Look for a tag in SVN if you
# want to package a stable release. - AdamW 2009/01
Source0:	http://prdownloads.sourceforge.net/%{name}/%{distname}
Source1:	http://kiax.sourceforge.net/img/kiax_logo_small.png
# Use system libraries. Wow, this buildsystem sucks - AdamW 2009/01
Patch0:		kiax-2.1-system_libs.patch
# Fixes for GCC 4.3 - AdamW 2009/01
Patch1:		kiax-2.0-gcc43.patch
# Fix for string literal errors - AdamW 2009/01
Patch2:		kiax-2.0-literal.patch
# Don't build with dottel, whatever the crap it is, as it's broken
# - AdamW 2009/01
Patch3:		kiax-2.1-disable_dottel.patch
BuildRequires:	imagemagick
BuildRequires:	iaxclient-devel
BuildRequires:	xpm-devel
BuildRequires:	libjson-devel
BuildRequires:	pkgconfig(speex)
BuildRequires:	portaudio-devel
BuildRequires:	gsm-devel
BuildRequires:	libqt4-devel
BuildRequires:	sqlite3-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	ldns-devel
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
Kiax is an IAX client application (a so called Softphone) which
allows PC users to make ordinary VoIP calls to Asterisk servers,
the same way as they do it with their hardware telephone. It aims
to provide a simple and user-friendly graphical interface and
desktop integration for calling, contact list, call register
management and easy configuration. That is - a simple to use IAX
Client.

%prep
%setup -q -n %{dirname}
%patch0 -p1 -b .system
%patch1 -p0 -b .gcc43
%patch2 -p1 -b .literal
%patch3 -p1 -b .dottel

%build
%qmake_qt4
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -d %{buildroot}%{_datadir}/%{name}/icons

install -m0755 gui/gui %{buildroot}%{_bindir}/%{name}
install -m0644 gui/icons/*.png %{buildroot}%{_datadir}/%{name}/icons/
install -m0644 gui/*.ui %{buildroot}%{_datadir}/%{name}

# fix some icons
convert %{SOURCE1} -geometry 48x48 %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert %{SOURCE1} -geometry 32x32 %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert %{SOURCE1} -geometry 16x16 %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Kiax
Comment=IAX softphone
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Network;Telephony;
EOF

%if %mdkversion < 200900
%post
%update_menus
%update_desktop_database
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_desktop_database
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png



%changelog
* Fri Feb 19 2010 Funda Wang <fwang@mandriva.org> 2.1-0.122.1mdv2010.1
+ Revision: 508460
- more gcc 43 fix

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild

* Tue Jan 06 2009 Adam Williamson <awilliamson@mandriva.org> 2.1-0.122.1mdv2009.1
+ Revision: 325192
- update file list
- update menu entry
- fd.o icons
- builds with qmake now
- update and fix buildrequires
- add dottel.patch: don't build with dottel support, it breaks
- add literal.patch: fix string literal errors
- add system_libs.patch: build against system libs
- drop old patches now irrelevant
- new license policy, correct license
- add conditionals for SVN build
- bump to current SVN (basically 2.1 beta 1, they don't do tarballs)

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild
    - rebuild
    - fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request
    - import kiax

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Sun Sep 17 2006 Oden Eriksson <oeriksson@mandriva.com> 0.8.51-3mdv2007.0
- rebuild

* Fri Sep 15 2006 Oden Eriksson <oeriksson@mandriva.com> 0.8.51-2mdv2007.0
- fix xdg menu

* Sun Jun 11 2006 Stefan van der Eijk <stefan@eijk.nu> 0.8.51-1mdk
- 0.8.51
- rediff patch0
- drop patch1 (merged upstream)

* Mon Dec 26 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.8.4-3mdk
- Remove redundant buildRequires

* Mon Apr 18 2005 Oden Eriksson <oeriksson@mandriva.com> 0.8.4-2mdk
- make it work on x86_64 (P1 by emosto at users.sourceforge.net)

* Fri Apr 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.8.4-1mdk
- 0.8.4
- fix P0
- use correct menu group
- note 0.8.4 segfaults on 10.1 x86_64

* Mon Apr 11 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.8.3-1mdk
- initial package
