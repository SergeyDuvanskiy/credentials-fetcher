%global major_version 1
%global minor_version 3
%global patch_version 5
 
# For handling bump release by rpmdev-bumpspec and mass rebuild
%global baserelease 0
 
Name:           credentials-fetcher
Version:        %{major_version}.%{minor_version}.%{patch_version}
Release:        %{baserelease}%{?dist}
Summary:        credentials-fetcher is a daemon that refreshes tickets or tokens periodically
 
License:        Apache-2.0
URL:            https://github.com/aws/credentials-fetcher
Source0:        credentials-fetcher-v.1.3.5.tar.gz

BuildRequires:  cmake3 make chrpath openldap-clients grpc-devel gcc-c++ glib2-devel jsoncpp-devel
BuildRequires:  openssl-devel zlib-devel protobuf-devel re2-devel krb5-devel systemd-devel
BuildRequires:  systemd-rpm-macros dotnet-sdk-6.0 grpc-plugins

%if 0%{?amzn} >= 2023
BuildRequires:  aws-sdk-cpp-devel aws-sdk-cpp aws-sdk-cpp-static
%endif
 
Requires: bind-utils openldap openldap-clients awscli dotnet-runtime-6.0 jsoncpp
# No one likes you i686
ExclusiveArch: x86_64 aarch64 s390x
 
# https://docs.fedoraproject.org/en-US/packaging-guidelines/CMake/
 
%description
This daemon creates and refreshes kerberos tickets, these
tickets can be used to launch new containers.
The gMSA feature can be implemented using this daemon.
Kerberos tickets are refreshed when tickets expire
or when a gMSA password changes.
The same method can be used to refresh other types of security tokens.
This spec file is specific to Fedora, use this file to rpmbuild on Fedora.
 
%prep
%setup -q -n credentials-fetcher-v.%{version}
# abseil-cpp LTS 20230125 requires at least C++14; string_view requires C++17:
sed -r -i 's/(std=c\+\+)11/\117/' CMakeLists.txt
 
%build
%cmake3
%cmake_build
%install
 
%cmake_install
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_removing_rpath
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_rpath_for_internal_libraries
chrpath --delete %{buildroot}/%{_sbindir}/credentials-fetcherd
 
%check
# TBD: Run tests from top-level directory
ctest3
 
%files
%{_sbindir}/credentials-fetcherd
%{_unitdir}/credentials-fetcher.service
%license LICENSE
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
%doc CONTRIBUTING.md NOTICE README.md
%attr(0700, -, -) %{_sbindir}/credentials_fetcher_utf16_private.exe
%attr(0700, -, -) %{_sbindir}/credentials_fetcher_utf16_private.runtimeconfig.json
%attr(0755, -, -) %{_sbindir}/krb5.conf

%changelog
* Mon Jan 15 2024 Sai Kiran Akula <saakla@amazon.com> - 1.3.5
- Create 1.3.5 release, added input validation
- Flag to handle unit tests

* Mon Dec 25 2023 Sai Kiran Akula <saakla@amazon.com> - 1.3.4
- Create 1.3.4 release, fix to skip directory check
- create custom mount points

* Tue Dec 12 2023 Sai Kiran Akula <saakla@amazon.com> - 1.3.3
- Fixes to add validation
- Add option to take custom paths

* Mon Dec 4 2023 Sai Kiran Akula <saakla@amazon.com> - 1.3.1
- Create 1.3.1 release, add file based loggin support
- Bug fixes for renewal logic

* Tue Nov 7 2023 Sai Kiran Akula <saakla@amazon.com> - 1.3.0
- Create 1.3.0 release, add support to retrieve credspec from s3
- Added dependency for aws-sdk-cpp

* Thu Aug 31 2023 Tom Callaway <spot@fedoraproject.org> - 1.2.0-3
- rebuild for abseil
 
* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Mon May 15 2023 Sai Kiran Akula <saakla@amazon.com> - 1.2.0
- Create 1.2.0 release
 
* Thu Mar 23 2023 Tom Callaway <spot@fedoraproject.org> - 1.1.0-7
- rebuild for new abseil-cpp
 
* Tue Mar 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.0-6
- Build as C++14, required by abseil-cpp 20230125
 
* Thu Feb 23 2023 Tom Callaway <spotaws@amazon.com> - 1.1.0-5
- fix build against boost 1.81 (bz2172636)
 
* Mon Feb 20 2023 Jonathan Wakely <jwakely@redhat.com> - 1.1.0-4
- Rebuilt for Boost 1.81
 
* Thu Feb 09 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.0-3
- Depend on dotnet-sdk-7.0; there is no longer an unversioned “dotnet” package
- Restore ppc64le support
 
* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Oct 27 2022 Sai Kiran Akula <saakla@amazon.com> - 1.1.0
- Create 1.1 release

* Mon Oct 24 2022 Samiullah Mohammed <samiull@amazon.com> - 1.0.0
- Add domainless gmsa

* Wed Oct 12 2022 Sai Kiran Akula <saakla@amazon.com> - 1.0.0
- Create 1.0 release

* Mon Sep 19 2022 Tom Callaway <spotaws@amazon.com> - 0.0.94-2
- rebuild for rawhide

* Sat Sep 10 2022 Samiullah Mohammed <samiull@amazon.com> - 0.0.94-1
- Replace mono with dotnet

* Mon Aug 29 2022 Tom Callaway <spotaws@amazon.com> - 0.0.94-1
- systemd clean up

* Mon Aug 22 2022 Sai Kiran Akula <saakla@amazon.com> - 0.0.93
- Add validation for read metadata file and rpm install require openldap-clients

* Wed Aug 10 2022 Samiullah Mohammed <samiull@amazon.com> - 0.0.92
- Move binaries to standard Linux directories

- Add directory paths as configurable variables in cmake
- Generate systemd service file from cmake

* Sun Aug 7 2022 Samiullah Mohammed <samiull@amazon.com> - 0.0.91
- Relocate binary, library files and change permissions

* Sat Jul 30 2022 Samiullah Mohammed <samiull@amazon.com> - 0.0.90
- add ctests and bump revision to 0.0.90

* Thu Jul 28 2022 Samiullah Mohammed <samiull@amazon.com> - 0.0.1
- Add mono-based utf16 decoder

* Tue Jul 12 2022 Samiullah Mohammed <samiull@amazon.com> - 0.0.1
- Resolve rpath for Fedora and change macros

* Sat Jun 18 2022 Sai Kiran Akula <saakla@amazon.com> - 0.0.1
- Refactor cmake for all the directories

* Thu Jun 16 2022 Samiullah Mohammed <samiull@amazon.com> - 0.0.1
- Compile subdirectory into a shared library

* Wed Jun 15 2022 Samiullah Mohammed <samiull@amazon.com> - 0.0.1
- Add daemon infra

* Wed Jun 8 2022 Samiullah Mohammed <samiull@amazon.com> - 0.0.1
- Fixes to rpm spec

* Mon Jun 6 2022 Samiullah Mohammed <samiull@amazon.com> - 0.0.1
- Initial commit
