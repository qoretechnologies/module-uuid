cmake_minimum_required(VERSION 3.5)

project(qore-uuid-module)

set (VERSION_MAJOR 1)
set (VERSION_MINOR 4)
set (VERSION_PATCH 2)

find_package(Qore 1.0 REQUIRED)

include_directories( ${CMAKE_SOURCE_DIR}/src )

# Check for C++11.
include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
if(COMPILER_SUPPORTS_CXX11)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
else()
    message(FATAL_ERROR "The compiler ${CMAKE_CXX_COMPILER} has no C++11 support. Please use a different C++ compiler.")
endif()

find_path(UUID_INCLUDE_DIR uuid.h PATH_SUFFIXES uuid ossp)

include(CheckFunctionExists)

if (WIN32 OR MSYS OR MINGW)
    set(CMAKE_REQUIRED_LINK_OPTIONS -lrpcrt4)
    set(CMAKE_REQUIRED_HEADERS "windows.h")
    set(CMAKE_SYSTEM_NAME Generic)
else()
    # Some systems include uuid automatically (OS X), others need the includes/library
    check_function_exists(uuid_unparse_lower HAVE_UUID)
    if (NOT HAVE_UUID)
        message ("-- Looking for libuuid")
        find_library(UUID_LIBRARY NAMES uuid)
        if (UUID_INCLUDE_DIR AND UUID_LIBRARY)
            message ("-- Found libuuid: ${UUID_LIBRARY}")
            set (HAVE_UUID true)
        else (UUID_INCLUDE_DIR AND UUID_LIBRARY)
            message(FATAL_ERROR "no libuuid found")
        endif (UUID_INCLUDE_DIR AND UUID_LIBRARY)
    endif (NOT HAVE_UUID)
endif()

include_directories(${UUID_INCLUDE_DIR})

set(QPP_SRC
    src/QC_UUID.qpp
)

set(CPP_SRC
    src/uuid-module.cpp
)

set(QMOD
)

qore_wrap_qpp_value(QPP_SOURCES DOXLIST QPP_DOX_SRC METALIST QPP_META_SRC ${QPP_SRC})

SET (module_name "uuid")

set(QORE_DOX_TMPL_SRC
  docs/mainpage.doxygen.tmpl
    docs/guide-uuidreleasenotes.dox.tmpl
)

add_library(${module_name} MODULE ${QPP_SOURCES} ${CPP_SRC})

if (DEFINED ENV{DOXYGEN_EXECUTABLE})
    set(DOXYGEN_EXECUTABLE $ENV{DOXYGEN_EXECUTABLE})
endif()

# Limit the public API reference to generated Qore declarations.
set(MODULE_DOX_INPUT ${CMAKE_BINARY_DIR}/mainpage.dox ${QPP_DOX_SRC})
list(APPEND MODULE_DOX_INPUT
    ${CMAKE_CURRENT_BINARY_DIR}/guide-uuidreleasenotes.dox
)
qore_external_binary_module(${module_name} "${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}" ${UUID_LIBRARY})
qore_user_modules("${QMOD}")

qore_dist("${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}")

# install qpp metadata files
if (COMMAND qore_install_qpp_metadata)
    qore_install_qpp_metadata(${module_name} ${QPP_META_SRC})
else()
    install(FILES ${QPP_META_SRC}
            DESTINATION ${CMAKE_INSTALL_DATADIR}/qore/metadata)
endif()

qore_config_info()

if (DOXYGEN_FOUND)
    qore_wrap_dox(QORE_DOX_SRC ${QORE_DOX_TMPL_SRC})
    add_custom_target(QORE_MOD_DOX_FILES DEPENDS ${QORE_DOX_SRC})
    add_dependencies(docs-module QORE_MOD_DOX_FILES)
endif()
