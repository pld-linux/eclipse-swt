#
# Conditional build:
%bcond_without	gnome		# build without gnome
%bcond_without	cairo		# build without cairo
#
%define   _buildid  200509290840
#define   _mver   M6
%define   _ver_major  3.1.1
%define   _ver_minor  0
%define   _ver_swt    3139
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
Summary(pl):	SWT - zestaw widgetów dla Javy
Name:		eclipse-swt
Version:	%{_ver_major}
#Release:	0.%{_mver}_%{_buildid}.1
Release:	0.1
License:	CPL v1.0
Group:		Libraries
#Source0:	http://download.eclipse.org/downloads/drops/S-%{_ver_major}%{_mver}-%{_buildid}/eclipse-sourceBuild-srcIncluded-%{_ver_major}%{_mver}.zip
Source0:	http://download.eclipse.org/eclipse/downloads/drops/R-%{_ver_major}-%{_buildid}/eclipse-sourceBuild-srcIncluded-%{_ver_major}.zip
# Source0-md5:	0d78d5f8afe767014a1cc69ee8c20869
Patch0:		%{name}-NULL.patch
Patch1:		%{name}-makefile.patch
Patch2:		%{name}-nognome.patch
URL:		http://www.eclipse.org/swt
BuildRequires:	atk-devel
%{?with_cairo:BuildRequires:  cairo-devel}
BuildRequires:  gtk+2-devel >= 2.0.0
BuildRequires:	ant >= 1.6.1
BuildRequires:	jdk >= 1.4
%{?with_gnome:BuildRequires:  libgnomeui-devel}
BuildRequires:	mozilla-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	unzip
BuildRequires:	zip
Requires:	jakarta-ant
Requires:	jdk >= 1.4
ExclusiveArch:	%{ix86} %{x8664} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SWT is a widget toolkit for Java designed to provide efficient,
portable access to the user-interface facilities of the operating
systems on which it is implemented.

%description -l pl
SWT to zestaw widgetów dla Javy zaprojektowany aby dostarczyæ wydajny,
przeno¶ny dostêp do udogodnieñ interfejsu u¿ytkownika na tych
systemach operacyjnych, na których zosta³ zaimplementowany.

%prep
%setup -q -c
JAVA_HOME=%{_libdir}/java
export JAVA_HOME
cd %{_swtsrcdir}
ant src.zip

%build
rm -rf swt
mkdir swt 
cd swt

unzip -x %{_builddir}/%{name}-%{version}/%{_swtsrcdir}/src.zip

patch -p0 < %{PATCH0}
patch -p0 < %{PATCH1}
%if %{without gnome}
patch -p0 < %{PATCH2}
%endif

JAVA_HOME=%{_libdir}/java
export JAVA_HOME
export JAVA_INC="-I$JAVA_HOME/include -I$JAVA_HOME/include/linux"
%{__make} -f make_linux.mak all \
    CC="%{__cc}" \
    CXX="%{__cxx}" \
    XTEST_LIB_PATH=%{_prefix}/X11R6/%{_lib} \
    OPT="%{rpmcflags}"

%if %{with cairo}
%{__make} -f make_linux.mak make_cairo \
    CC="%{__cc}" \
    CXX="%{__cxx}" \
    XTEST_LIB_PATH=%{_prefix}/X11R6/%{_lib} \
    OPT="%{rpmcflags}"
%endif

%{__make} -f make_linux.mak make_mozilla \
    CC="%{__cc}" \
    CXX="%{__cxx}" \
    XTEST_LIB_PATH=%{_prefix}/X11R6/%{_lib} \
    OPT="%{rpmcflags}"

#cp library/* .
#{__make} -f make_linux.mak make_mozilla \
#    OPT="%{rpmcflags}"

cd ../%{_swtsrcdir}
ant build.jars

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/swt/%{_swtgtkdir}_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch} \
	$RPM_BUILD_ROOT%{_javadir}

install %{_swtsrcdir}/swt.jar $RPM_BUILD_ROOT%{_javadir}

cd swt
install libswt-*.so \
	$RPM_BUILD_ROOT%{_libdir}/swt/%{_swtgtkdir}_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch}

ln -sf %{_libdir}/swt/%{_swtgtkdir}_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch}/libswt-atk-gtk-%{_ver_swt}.so \
	$RPM_BUILD_ROOT%{_libdir}/swt
ln -sf %{_libdir}/swt/%{_swtgtkdir}_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch}/libswt-awt-gtk-%{_ver_swt}.so \
	$RPM_BUILD_ROOT%{_libdir}/swt
ln -sf %{_libdir}/swt/%{_swtgtkdir}_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch}/libswt-gtk-%{_ver_swt}.so \
	$RPM_BUILD_ROOT%{_libdir}/swt
ln -sf %{_libdir}/swt/%{_swtgtkdir}_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch}/libswt-mozilla-gtk-%{_ver_swt}.so \
	$RPM_BUILD_ROOT%{_libdir}/swt
ln -sf %{_libdir}/swt/%{_swtgtkdir}_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch}/libswt-pi-gtk-%{_ver_swt}.so \
	$RPM_BUILD_ROOT%{_libdir}/swt

%if %{with cairo}
install libcairo.so* $RPM_BUILD_ROOT%{_libdir}/swt
%endif

%if %{with gnome}
ln -sf %{_libdir}/swt/%{_swtgtkdir}_%{_ver_major}.%{_ver_minor}/os/linux/%{_eclipse_arch}/libswt-gnome-gtk-%{_ver_swt}.so \
	$RPM_BUILD_ROOT%{_libdir}/swt
%endif

install *.html $RPM_BUILD_ROOT%{_libdir}/swt
cp -rf about_files $RPM_BUILD_ROOT%{_libdir}/swt

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
%attr(755,root,root) %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-awt-gtk-*.so
%if %{with gnome}
%attr(755,root,root) %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-gnome-gtk-*.so
%endif
%attr(755,root,root) %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-gtk-*.so
#%attr(755,root,root) %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-kde-gtk*.so
%attr(755,root,root) %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-mozilla-gtk-*.so
%attr(755,root,root) %{_libdir}/swt/%{_swtgtkdir}_*.*.*/os/linux/%{_eclipse_arch}/libswt-pi-gtk-*.so
