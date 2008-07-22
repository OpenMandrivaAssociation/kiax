Summary:	IAX client application (a so called Softphone)
Name:		kiax
Version:	0.8.51
Release:	%mkrel 6
License:	GPL
Group:		Graphical desktop/KDE
URL:		http://kiax.org/
Source0:	http://prdownloads.sourceforge.net/kiax/%{name}-%{version}-src.tar.bz2
Source1:	http://kiax.sourceforge.net/img/kiax_logo_small.png
Patch0:		kiax-0.8.4-system_iaxclient_libs.diff.bz2
Patch1:		kiax-0.8.51-iaxwrapper.cpp.patch
BuildRequires:	ImageMagick
BuildRequires:	iaxclient-devel
BuildRequires:	kdelibs-devel
BuildRequires:	xpm-devel
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

%setup -q -n %{name}-%{version}-src
%patch0 -p1
%patch1 -p1

%build
export QTDIR=%{_prefix}/lib/qt3
export KDEDIR=%{_prefix}
export LD_LIBRARY_PATH="$QTDIR:/%{_lib}:$LD_LIBRARY_PATH"
export PATH="$KDEDIR/bin:$PATH"

sh configure --prefix=%{_prefix} --targetos=mandrake

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
#export DONT_STRIP=1

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}
install -d %{buildroot}%{_datadir}/%{name}/icons
install -d %{buildroot}%{_datadir}/%{name}/i18n

install -m0755 bin/%{name} %{buildroot}%{_bindir}/
install -m0644 icons/*.png %{buildroot}%{_datadir}/%{name}/icons/
install -m0644 i18n/*.qm %{buildroot}%{_datadir}/%{name}/i18n/

# fix some icons
convert %{SOURCE1} -geometry 48x48 %{buildroot}%{_liconsdir}/%{name}.png
convert %{SOURCE1} -geometry 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert %{SOURCE1} -geometry 16x16 %{buildroot}%{_miconsdir}/%{name}.png

# fix mandrake menu entry

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Kiax
Comment=Kiax is an IAX client application (a so called Softphone)
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet-VideoConference;Network;Telephony;
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
%doc CHANGELOG COPYING README
%{_bindir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop

