# NOTE
# - build instructions: http://www.eclipse.org/swt/faq.php#howbuilddll
#
# Conditional build:
%bcond_without	gnome		# build without gnome
%bcond_without	xulrunner		# build without xulrunner
%bcond_without	glx		# build without glx
%bcond_with	cairo		# build with cairo
#
%define   _buildid  200706251500
#define   _mver   M6
%define   _ver_major  3.3
%define   _ver_minor  0
%define   _ver_swt    3346
%define   _ver    %{_ver_major}.%{_ver_minor}

%ifarch %{x8664}
%define _swtsrcdir  plugins/org.eclipse.swt.gtk.linux.x86_64
%define _swtgtkdir  plugins/org.eclipse.swt.gtk.linux.x86_64
%endif

%ifarch ppc
%define _swtsrcdir  plugins/org.eclipse.swt.gtk.linux.ppc
%define _swtgtkdir  plugins/org.eclipse.swt.gtk.linux.ppc
%endif

%ifarch %{ix86}
%define _swtsrcdir  plugins/org.eclipse.swt.gtk.linux.x86
%define _swtgtkdir  plugins/org.eclipse.swt.gtk.linux.x86
%endif

%define   _eclipse_arch %(echo %{_target_cpu} | sed 's/i.86/x86/;s/athlon/x86/;s/pentium./x86/')
%define   no_install_post_chrpath   1
%ifarch %{x8664}
%define         _noautostrip  .*\\.so
%endif

Summary:	SWT - a widget toolkit for Java
Summary(pl.UTF-8):	SWT - zestaw widgetów dla Javy
Name:		eclipse-swt
Version:	%{_ver_major}
#Release:	0.%{_mver}_%{_buildid}.1
Release:	1
License:	CPL v1.0
Group:		Libraries
#Source0:	http://download.eclipse.org/downloads/drops/S-%{_ver_major}%{_mver}-%{_buildid}/eclipse-sourceBuild-srcIncluded-%{_ver_major}%{_mver}.zip
# Source0-md5:	91c688221479986dbdd7d1a0771f04cc
Source0:	http://download.eclipse.org/eclipse/downloads/drops/R-%{_ver_major}-%{_buildid}/eclipse-sourceBuild-srcIncluded-%{version}.zip
Patch0:		%{name}-NULL.patch
URL:		http://www.eclipse.org/swt
%{?with_glx:BuildRequires:	OpenGL-devel}
BuildRequires:	ant >= 1.6.1
BuildRequires:	atk-devel
%{?with_cairo:BuildRequires:  cairo-devel}
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	jdk >= 1.4
%{?with_gnome:BuildRequires:  libgnomeui-devel}
%{?with_xulrunner:BuildRequires:	libstdc++-devel}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	unzip
%{?with_xulrunner:BuildRequires:	xulrunner-devel}
BuildRequires:	zip
Requires:	ant
Requires:	jdk >= 1.4
ExclusiveArch:	%{ix86} %{x8664} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SWT is a widget toolkit for Java designed to provide efficient,
portable access to the user-interface facilities of the operating
systems on which it is implemented.

%description -l pl.UTF-8
SWT to zestaw widgetów dla Javy zaprojektowany aby dostarczyć wydajny,
przenośny dostęp do udogodnień interfejsu użytkownika na tych
systemach operacyjnych, na których został zaimplementowany.

%prep
%setup -q -c
%ant -f %{_swtsrcdir}/build.xml src.zip
mkdir swt
cd swt
%{__unzip} -qq -o ../%{_swtsrcdir}/src.zip
%patch0 -p0

%build
%{__make} -f make_linux.mak -C swt \
	make_swt make_atk \
	%{?with_glx:make_glx} \
	%{?with_gnome:make_gnome} \
	%{?with_cairo:make_cairo} \
	%{?with_xulrunner:make_xulrunner XULRUNNER_INCLUDES="$(pkg-config --cflags xulrunner-xpcom)"} \
	JAVA_HOME="%{java_home}" \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	XTEST_LIB_PATH=%{_prefix}/X11R6/%{_lib} \
	OPT="%{rpmcflags}"

%ant -f %{_swtsrcdir}/build.xml build.jars

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
install %{_swtsrcdir}/swt.jar $RPM_BUILD_ROOT%{_javadir}

dir=%{_libdir}/swt/%{_swtgtkdir}_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch}
install -d $RPM_BUILD_ROOT$dir
for a in swt/libswt-*.so; do
	install $a $RPM_BUILD_ROOT$dir
	lib=${a##*/}
	ln -sf ${dir#%{_libdir}/swt/}/$lib $RPM_BUILD_ROOT%{_libdir}/swt
done

%if %{with cairo}
install swt/libcairo.so* $RPM_BUILD_ROOT%{_libdir}/swt
%endif

install swt/*.html $RPM_BUILD_ROOT%{_libdir}/swt
cp -a swt/about_files $RPM_BUILD_ROOT%{_libdir}/swt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/swt
%dir %{_libdir}/swt/%{_swtgtkdir}_*.*.*
%dir %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os
%dir %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux
%dir %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}
%{_javadir}/swt.jar
%{_libdir}/swt/about_files
%{_libdir}/swt/about.html
%{_libdir}/swt/libswt-*-%{_ver_swt}.so
%attr(755,root,root) %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-atk-gtk-*.so
%{?with_glx:%attr(755,root,root) %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-glx-gtk-*.so}
%{?with_gnome:%attr(755,root,root) %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-gnome-gtk-*.so}
%attr(755,root,root) %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-gtk-*.so
%attr(755,root,root) %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-pi-gtk-*.so
%{?with_xulrunner:%attr(755,root,root) %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-xulrunner-gtk-*.so}
