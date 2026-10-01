# Copyright (C) 2026 Qore Technologies, s.r.o.
# SPDX-License-Identifier: MIT
# Use the pinned source epoch for RPM headers and installed file timestamps.
%global source_date_epoch_from_changelog 1
%global use_source_date_epoch_as_buildtime 1
%if v"%{rpmversion}" >= v"4.20"
%global build_mtime_policy clamp_to_source_date_epoch
%else
%global clamp_mtime_to_source_date_epoch 1
%endif
%bcond_without tests
%bcond_without docs
Name: qore-uuid-module
Version: 1.4.2
Release: 2%{?dist}
Summary: UUID generation and parsing for Qore
License: MIT
URL: https://github.com/qoretechnologies/module-uuid
Source0: %{name}-%{version}.tar.xz
BuildRequires: cmake >= 3.5
BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: pkgconfig(uuid)
BuildRequires: qore-devel >= 3.0.0~
BuildRequires: qore-rpm-macros >= 3.0.0~
%if %{with docs}
BuildRequires: doxygen
BuildRequires: /usr/bin/hardlink
%endif

%description
Native Qore module for generating and parsing universally unique identifiers.

%if %{with docs}
%package doc
Summary: UUID module reference documentation
BuildArch: noarch
%description doc
API reference and examples for Qore's UUID module.
%endif

%prep
%autosetup
%build
%{?set_build_flags}
. %{_rpmconfigdir}/qore/module-env.sh
qore_set_source_prefix_maps "%{qore_debug_source_dir}"
cmake -S . -B build -G 'Unix Makefiles' \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} \
  -DCMAKE_SKIP_RPATH=ON -DCMAKE_IGNORE_PREFIX_PATH=/usr/local \
  -DQore_DIR=%{_libdir}/cmake/Qore -DQORE_EXECUTABLE=/usr/bin/qore \
  -DQORE_QPP_EXECUTABLE=/usr/bin/qpp \
  -DCMAKE_DISABLE_FIND_PACKAGE_Doxygen=%{!?with_docs:ON}%{?with_docs:OFF}
cmake --build build -- %{?_smp_mflags}
%if %{with docs}
cmake --build build --target docs -- %{?_smp_mflags}
%endif
%install
DESTDIR=%{buildroot} cmake --install build
chmod 755 %{buildroot}%{_libdir}/qore-modules/uuid-api-*.qmod
%if %{with docs}
install -d %{buildroot}%{_docdir}/%{name}-doc
cp -a build/docs/uuid/html %{buildroot}%{_docdir}/%{name}-doc/
hardlink -t -O %{buildroot}%{_docdir}/%{name}-doc
%endif
%check
%if %{with tests}
. %{_rpmconfigdir}/qore/module-env.sh
/usr/bin/qore -b --enable-debug -l "$PWD/build/uuid-api-$(/usr/bin/qore --latest-module-api).qmod" test/uuid-test.qtest -v
%endif
%files
%license COPYING.MIT
%doc README
%{_libdir}/qore-modules/uuid-api-*.qmod
%dir %{_datadir}/qore/metadata/uuid
%{_datadir}/qore/metadata/uuid/*.meta.json
%if %{with docs}
%files doc
%license COPYING.MIT
%doc %{_docdir}/%{name}-doc/
%endif
%changelog
* Thu Oct 01 2026 David Nichols <david@qore.org> - 1.4.2-2
- Use the packaged SDK, generated ABI requirements and offline module tests.
