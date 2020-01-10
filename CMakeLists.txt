cmake_minimum_required(VERSION 2.8.10 FATAL_ERROR)
project(gsd)

set(PYTHON_MODULE_BASE_DIR "gsd")

add_subdirectory(CMake)
include(CFlagsSetup)
include(LinterSetup)

#############################################################################################
# Find libraries
include(PythonSetup)
include_directories(${PYTHON_INCLUDE_DIR})

#############################################################################################
# set the default install prefix
SET(CMAKE_INSTALL_PREFIX ${PYTHON_SYSTEM_SITE} CACHE PATH "Python site installation directory" FORCE)
message(STATUS "Setting installation site dir: ${CMAKE_INSTALL_PREFIX}")

if (WIN32)
add_compile_definitions(_CRT_SECURE_NO_WARNINGS)
endif()

#############################################################################################
### Add project subdirs
include_directories(gsd)
add_subdirectory(gsd)
add_subdirectory(scripts)
