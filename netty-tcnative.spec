%{?_javapackages_macros:%_javapackages_macros}
%global namedreltag .Fork2
%global namedversion %{version}%{?namedreltag}

Name:           netty-tcnative
Version:        1.1.30
Release:        6%{?dist}
Summary:        Fork of Tomcat Native with improved OpenSSL and mavenized build
License:        ASL 2.0
Group:		Development/Java
URL:            https://github.com/netty/netty/wiki/Forked-Tomcat-Native
Source0:        https://github.com/netty/netty-tcnative/archive/%{name}-%{namedversion}.tar.gz
Source1:        CheckLibrary.java
Patch1:         fixLibNames.patch.in
Patch2:         i388aprFix.patch
Patch3:         %{name}-1.1.30-openssl.patch

BuildRequires:  maven-local
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  glibc-devel
BuildRequires:  apr-devel
BuildRequires:  openssl-devel
BuildRequires:  maven-antrun-plugin
BuildRequires:  maven-hawtjni-plugin
BuildRequires:  maven-plugin-build-helper
BuildRequires:  maven-plugin-bundle
BuildRequires:  maven-source-plugin
#parent pom is needed
BuildRequires:  netty
BuildRequires:  sonatype-oss-parent
BuildRequires: mvn(kr.motd.maven:os-maven-plugin)


%description
netty-tcnative is a fork of Tomcat Native. It includes a set of changes
contributed by Twitter, Inc, such as:
 *  Simplified distribution and linkage of native library
 *  Complete mavenization of the project
 *  Improved OpenSSL support
To minimize the maintenance burden, we create a dedicated branch for each
stable upstream release and apply our own changes on top of it, while
keeping the number of maintained branches to minimum


%package javadoc
Summary:   API documentation for %{name}
Group:     Documentation
BuildArch: noarch

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{name}-%{namedversion}
patch=`mktemp`
sed "s;@PATH@;%{_libdir}/%{name};g" < %{PATCH1} > $patch
patch -p1 < $patch
%patch2 -p1
#% patch3 -p1 -b .openssl


%build
%setup_compile_flags
%mvn_build -f

%install
%mvn_install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/
cp target/native-build/target/lib/lib%{name}-%{namedversion}.so $RPM_BUILD_ROOT%{_libdir}/%{name}/lib%{name}.so


%check
javac -d . -cp $RPM_BUILD_ROOT%{_jnidir}/%{name}/%{name}.jar %{SOURCE1}
#don't know how to test load(path) without more and more patching, however the test class can be used for manual testing
#java -cp .:$RPM_BUILD_ROOT%%{_jnidir}/%%{name}/%%{name}.jar CheckLibrary


%files -f .mfiles
%dir %{_libdir}/%{name}
%dir %{_jnidir}/%{name}
%dir %{_mavenpomdir}/%{name}
%{_libdir}/%{name}/lib%{name}.so

%files javadoc -f .mfiles-javadoc

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 04 2017 Merlin Mathesius <mmathesi@redhat.com> - 1.1.30-5
- Update to use OpenSSL-1.0 compatibility package to fix FTBFS (BZ#1406480).

* Mon Dec 19 2016 Merlin Mathesius <mmathesi@redhat.com> - 1.1.30-4
- Add missing BuildRequires to fix FTBFS (BZ#1406480).

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 13 2015 Jiri Vanek <jvanek@redhat.com> - 1.1.30-2
- adapted to parent pom, enabled kr.motd.maven:os-maven-plugin and added buildrequires dependence 

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 18 2015 Jiri Vanek <jvanek@redhat.com> - 1.1.30-1
- removed manual requires

* Thu Jan 29 2015 Jiri Vanek <jvanek@redhat.com> - 1.1.30-0
- initial build
