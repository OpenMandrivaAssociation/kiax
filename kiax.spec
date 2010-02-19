%define svn	122
%define rel	2

%if %svn
%define release		%mkrel 0.%{svn}.1
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
BuildRequires:	libspeex-devel
BuildRequires:	portaudio-devel
BuildRequires:	gsm-devel
BuildRequires:	libqt4-devel
BuildRequires:	sqlite3-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	ldns-devel
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

