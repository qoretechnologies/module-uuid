/* indent-tabs-mode: nil -*- */
/*
  uuid Qore module

  Copyright (C) 2010 - 2026 David Nichols

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

#include "uuid-module.h"

static void uuid_module_init(QoreModuleInitContext& ctx, ExceptionSink& xsink);
static void uuid_module_ns_init(QoreNamespace* rns, QoreNamespace* qns, ExceptionSink& xsink);
static void uuid_module_delete();

// the module's namespace; purged when the module is deleted (see QoreModuleInfo::ns)
QoreNamespace UNS("Qore::UUID");

extern "C" DLLEXPORT void uuid_qore_module_desc(QoreModuleInfo& mod_info) {
    mod_info.name = "uuid";
    mod_info.version = PACKAGE_VERSION;
    mod_info.desc = "uuid module";
    mod_info.author = "David Nichols";
    mod_info.url = "http://qore.org";
    mod_info.api_major = QORE_MODULE_API_MAJOR;
    mod_info.api_minor = QORE_MODULE_API_MINOR;
    mod_info.init = uuid_module_init;
    mod_info.ns_init = uuid_module_ns_init;
    mod_info.del = uuid_module_delete;
#ifdef QORE_HAS_MODULE_NS_PURGE
    // the namespace is purged when the module is deleted, before the types are freed (see QoreModuleInfo::ns)
    mod_info.ns = &UNS;
#endif
    mod_info.license = QL_MIT;
    mod_info.license_str = "MIT";
}

DLLLOCAL QoreClass* initUUIDClass(QoreNamespace &ns);

static void uuid_module_init(QoreModuleInitContext& ctx, ExceptionSink& xsink) {
   // setup namespace
   QoreClass *QC_UUID = initUUIDClass(UNS);
   UNS.addSystemClass(QC_UUID);
}

static void uuid_module_ns_init(QoreNamespace* rns, QoreNamespace* qns, ExceptionSink& xsink) {
   qns->addNamespace(UNS.copy());
}

void uuid_module_delete() {
}
