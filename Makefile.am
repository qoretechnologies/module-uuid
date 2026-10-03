AUTOMAKE_OPTIONS = foreign

SUBDIRS = src

noinst_HEADERS = src/uuid-module.h

EXTRA_DIST = COPYING.MIT COPYING.LGPL AUTHORS README \
	RELEASE-NOTES \
	src/QC_UUID.qpp \
	test/uuid-test.q \
	qore-uuid-module.spec

TESTSCRIPTS=test/uuid-test.q

ACLOCAL_AMFLAGS=-I m4

if COND_DOXYGEN
DOX = uuid
DOXYGEN_QORE_API_FILTER=docs/doxygen-api-filter.q
DOXYGEN_OUTPUT=docs/uuid/html
DOXYFILES = docs/doxyfile docs/mainpage.doxygen
DOXYFILES += docs/guide-uuidreleasenotes.dox
QDX = qdx
DX_CLEANFILES = ${DOXYFILES}

docs/uuid/html: $(DOXYFILES)
	cd docs; $(DOXYGEN_CMD) doxyfile;
	$(QDX) --post $(DOXYGEN_OUTPUT)/*html
	$(QDX) --post $(DOXYGEN_OUTPUT)/search/*html

doxygen-doc: $(DOXYGEN_OUTPUT)

EXTRA_DIST += $(DOXYGEN_OUTPUT)

html-local: $(DOXYGEN_OUTPUT)

install-html-local:
	for dox in $(DOX); do $(MKDIR_P) $(DESTDIR)$(datadir)/$(PACKAGE)/docs/$$dox/html/search; done
	for dir in $(DOXYGEN_OUTPUT); do \
	   for f in $$dir/*; do if [ -f $$f ]; then $(INSTALL_DATA) $$f $(DESTDIR)$(datadir)/$(PACKAGE)/$$dir; fi; done; \
	   for f in $$dir/search/*; do $(INSTALL_DATA) $$f $(DESTDIR)$(datadir)/$(PACKAGE)/$$dir/search; done; \
	done

clean-local:
	$(RM) -rf $(DOXYGEN_OUTPUT)

uninstall-local:
	$(RM) -rf $(DESTDIR)$(datadir)/$(PACKAGE)/docs

else
doxygen-doc:
	echo no doxygen support
endif

mostlyclean-local:
	$(RM) -rf ${DOXYGEN_OUTPUT} ${DX_CLEANFILES}

libtool: $(LIBTOOL_DEPS)
	$(SHELL) ./config.status --recheck

docs/mainpage.doxygen: docs/mainpage.doxygen.tmpl
	$(QDX) -d $< $@

docs/guide-uuidreleasenotes.dox: docs/guide-uuidreleasenotes.dox.tmpl
	$(QDX) -d $< $@

docs/doxyfile: docs/doxyfile.tmpl
	sed -e s/__VERSION__/${VERSION}/ -e s:__USERMODDIR__:${usermoddir}: $< > $@

tests:
	@for i in $(TESTSCRIPTS); do qore $$i --format=plain; done

tests-ci:
	@for i in $(TESTSCRIPTS); do qore $$i --format=junit --verbose; done

# Documentation guide sources shipped with the module.
EXTRA_DIST += docs/guide-uuidreleasenotes.dox.tmpl
