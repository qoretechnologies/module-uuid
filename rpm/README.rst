RPM packaging
=============

Copyright 2026 Qore Technologies, s.r.o.

The canonical qore-uuid-module.spec supports Fedora, Enterprise Linux and
openSUSE. It requires the Qore 3.0 SDK and qore-rpm-macros from the same repository.
The default build includes module tests and a separate documentation package.
Dependencies on the installed Qore ABI and SDK version are generated from the
built module; do not replace them with an unversioned qore dependency.

Prepare a pinned source bundle with qore-packaging, then build it in the target
distribution with networking disabled::

    python3 tools/packaging.py prepare --repo ../module-uuid --ref COMMIT \
      --name qore-uuid-module --version 1.4.2 \
      --spec qore-uuid-module.spec --output work/uuid-source
    python3 tools/build-local.py --source work/uuid-source \
      --image TARGET_SDK_IMAGE --output results/uuid-build --jobs 2

These commands run from the qore-packaging repository. Source preparation uses
the committed tree. Install the SDK's language documentation index for complete
Doxygen cross-references. --without docs and --without tests are available for
local diagnosis; repository qualification uses the defaults and also runs the
suite against installed RPMs outside the checkout. Native modules retain the
distribution's normal ELF stripping and separate debug packages.

``Source0`` identifies the generated archive in the OBS source package.
``source-manifest.json`` records the exact Git commit and SHA-256 hashes; retain
that manifest with the source RPM when reproducing a particular build.

API documentation is built with warnings treated as errors. The default RPM
checks also exercise CMake's uninstall manifest handling, including spaces,
symlinks, missing files and invalid paths. For a manual staged source install::

    DESTDIR=/tmp/uuid-stage cmake --install build
    DESTDIR=/tmp/uuid-stage cmake --build build --target uninstall

Uninstall uses the configured build directory's manifest and preserves parent
directories. Manage installed RPMs with the distribution's package manager.

The Autotools ``make tests`` and ``make tests-ci`` targets use the same current
``test/uuid-test.qtest`` suite with Qore debugging enabled. JUnit output from
``make tests-ci`` additionally requires the XML module.
