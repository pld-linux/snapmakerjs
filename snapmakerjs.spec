Summary:	Snapmaker 3-in-1 Software for 3D Printing, Laser Engraving and CNC Cutting
Name:		snapmakerjs
Version:	2.7.1
Release:	3
License:	MIT
Group:		Applications
Source0:	https://s3-us-west-2.amazonaws.com/snapmaker.com/download/snapmakerjs/%{name}-%{version}-linux-x64.tar.gz
# Source0-md5:	f4b1e550664f7f8e4da2e29ab1f0c4ff
Source2:	%{name}.desktop
Source3:	%{name}.png
URL:		https://snapmaker.com/
BuildRequires:	ImageMagick
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		no_install_post_check_shebangs	1
%define		_enable_debug_packages	0

%description
Snapmaker 3-in-1 Software for 3D Printing, Laser Engraving and CNC
Cutting.

%prep
%setup -q -T -b0 -n %{name}-%{version}-linux-x64

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/%{name},%{_bindir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps

cp -a * $RPM_BUILD_ROOT%{_libdir}/%{name}
ln -s %{_libdir}/%{name}/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

for i in 16 24 32 48 64 96 128 ; do
  install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps
  convert -geometry ${i}x${i} %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps/%{name}.png
done

cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps

# _install_post_check_shebangs can't cope with filenames with spaces
find $RPM_BUILD_ROOT -name "Apache License.txt" -print0 | xargs -0 %{__rm}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%triggerpostun -- snapmakerjs < 2.6.1-1
%groupremove snapmaker

%files
%defattr(644,root,root,755)
%doc LICENSE.electron.txt LICENSES.chromium.html
%attr(755,root,root) %{_bindir}/%{name}*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/locales
%dir %{_libdir}/snapmakerjs/resources
%{_libdir}/%{name}/resources/electron.asar
%dir %{_libdir}/snapmakerjs/resources/app
%{_libdir}/snapmakerjs/resources/app/app
%{_libdir}/snapmakerjs/resources/app/electron-app
%{_libdir}/snapmakerjs/resources/app/node_modules
%{_libdir}/snapmakerjs/resources/app/*.js
%{_libdir}/snapmakerjs/resources/app/*.json
%dir %{_libdir}/snapmakerjs/resources/app/resources
%{_libdir}/snapmakerjs/resources/app/resources/fonts
%dir %{_libdir}/snapmakerjs/resources/app/resources/CuraEngine
%{_libdir}/snapmakerjs/resources/app/resources/CuraEngine/Config
%dir %{_libdir}/snapmakerjs/resources/app/resources/CuraEngine/3.6
%dir %{_libdir}/snapmakerjs/resources/app/resources/CuraEngine/3.6/Linux
%attr(755,root,root) %{_libdir}/snapmakerjs/resources/app/resources/CuraEngine/3.6/Linux/CuraEngine
%dir %{_libdir}/snapmakerjs/resources/app/server
%{_libdir}/snapmakerjs/resources/app/server/index.js
%dir %{_libdir}/snapmakerjs/resources/app/server/i18n
%lang(cs) %{_libdir}/snapmakerjs/resources/app/server/i18n/cs
%lang(de) %{_libdir}/snapmakerjs/resources/app/server/i18n/de
%lang(en) %{_libdir}/snapmakerjs/resources/app/server/i18n/en
%lang(es) %{_libdir}/snapmakerjs/resources/app/server/i18n/es
%lang(fr) %{_libdir}/snapmakerjs/resources/app/server/i18n/fr
%lang(hu) %{_libdir}/snapmakerjs/resources/app/server/i18n/hu
%lang(it) %{_libdir}/snapmakerjs/resources/app/server/i18n/it
%lang(ja) %{_libdir}/snapmakerjs/resources/app/server/i18n/ja
%lang(pt_BR) %{_libdir}/snapmakerjs/resources/app/server/i18n/pt-br
%lang(ru) %{_libdir}/snapmakerjs/resources/app/server/i18n/ru
%lang(zh_CN) %{_libdir}/snapmakerjs/resources/app/server/i18n/zh-cn
%lang(zh_TW) %{_libdir}/snapmakerjs/resources/app/server/i18n/zh-tw
%{_libdir}/snapmakerjs/resources/app/server/views
%{_libdir}/%{name}/*.dat
%{_libdir}/%{name}/*.bin
%{_libdir}/%{name}/*.pak
%attr(755,root,root) %{_libdir}/%{name}/libffmpeg.so
%attr(755,root,root) %{_libdir}/%{name}/libnode.so
%attr(755,root,root) %{_libdir}/%{name}/snapmakerjs
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*x*/apps/%{name}.png
