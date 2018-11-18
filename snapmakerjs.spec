Summary:	Snapmaker 3-in-1 Software for 3D Printing, Laser Engraving and CNC Cutting
Name:		snapmakerjs
Version:	2.4.6
Release:	1
License:	MIT
Group:		Applications
Source0:	https://s3-us-west-2.amazonaws.com/snapmaker.com/download/snapmakerjs/%{name}-%{version}-linux-x64.tar.gz
# Source0-md5:	cf936afda42bb1df344d62d5912d8e17
Source1:	https://s3-us-west-2.amazonaws.com/snapmaker.com/download/snapmakerjs/%{name}-%{version}-linux-ia32.tar.gz
# Source1-md5:	e463d0b8d5440e6b6a4e22b445e08520
Source2:	%{name}.desktop
Source3:	%{name}.png
URL:		https://snapmaker.com/
BuildRequires:	ImageMagick
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Snapmaker 3-in-1 Software for 3D Printing, Laser Engraving
and CNC Cutting.

%prep
%ifarch %{x8664}
%setup -q -T -b0 -n %{name}-%{version}-linux-x64
%endif
%ifarch %{ix86}
%setup -q -T -b1 -n %{name}-%{version}-linux-ia32
%endif

%build
%{__sed} -i -e 's|./sessions|/var/lib/snapmakerjs/sessions|' \
	-e 's|./fonts|/var/lib/snapmakerjs/fonts|' resources/app/app/index.js

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/%{name},%{_bindir},%{_desktopdir},/etc/snapmakerjs} \
	$RPM_BUILD_ROOT{%{_iconsdir}/hicolor/256x256/apps,/var/lib/snapmakerjs/_cache}

cp -a * $RPM_BUILD_ROOT%{_libdir}/%{name}
ln -s %{_libdir}/%{name}/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/resources/app/web/images/_cache
ln -s /var/lib/snapmakerjs/_cache $RPM_BUILD_ROOT%{_libdir}/%{name}/resources/app/web/images/_cache

%{__mv} $RPM_BUILD_ROOT%{_libdir}/snapmakerjs/resources/app/CuraEngine/Config \
	$RPM_BUILD_ROOT/etc/snapmakerjs/CuraEngine
ln -s /etc/snapmakerjs/CuraEngine $RPM_BUILD_ROOT%{_libdir}/snapmakerjs/resources/app/CuraEngine/Config

for i in 16 24 32 48 64 96 128 ; do
  install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps
  convert -geometry ${i}x${i} %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps/%{name}.png
done

cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps


%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 184 snapmaker

%post
%update_icon_cache hicolor

%banner %{name} <<-EOF
You need to be a member of snapmaker group to use all features of the program!
EOF

%postun
if [ "$1" = "0" ]; then
       %groupremove snapmaker
fi
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc LICENSE.electron.txt LICENSES.chromium.html
%dir /etc/snapmakerjs
%dir %attr(775,root,snapmaker) /etc/snapmakerjs/CuraEngine
%attr(664,root,snapmaker) %config %verify(not md5 mtime size) /etc/snapmakerjs/CuraEngine/*
%attr(755,root,root) %{_bindir}/%{name}*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/locales
%dir %{_libdir}/snapmakerjs/resources
%{_libdir}/%{name}/resources/electron.asar
%dir %{_libdir}/snapmakerjs/resources/app
%{_libdir}/snapmakerjs/resources/app/app
%{_libdir}/snapmakerjs/resources/app/electron-app
%{_libdir}/snapmakerjs/resources/app/node_modules
%{_libdir}/snapmakerjs/resources/app/web
%{_libdir}/snapmakerjs/resources/app/*.js
%{_libdir}/snapmakerjs/resources/app/*.json
%dir %{_libdir}/snapmakerjs/resources/app/CuraEngine
%{_libdir}/snapmakerjs/resources/app/CuraEngine/Config
%dir %{_libdir}/snapmakerjs/resources/app/CuraEngine/2.7
%dir %{_libdir}/snapmakerjs/resources/app/CuraEngine/2.7/Linux-x64
%attr(755,root,root) %{_libdir}/snapmakerjs/resources/app/CuraEngine/2.7/Linux-x64/CuraEngine
%{_libdir}/%{name}/*.dat
%{_libdir}/%{name}/*.bin
%{_libdir}/%{name}/*.pak
%attr(755,root,root) %{_libdir}/%{name}/libffmpeg.so
%attr(755,root,root) %{_libdir}/%{name}/libnode.so
%attr(755,root,root) %{_libdir}/%{name}/snapmakerjs
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*x*/apps/%{name}.png
%dir %attr(1777,root,root) /var/lib/%{name}
%dir %attr(1777,root,root) /var/lib/%{name}/_cache
