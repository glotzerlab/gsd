cmake_minimum_required(VERSION 2.8.10 FATAL_ERROR)
project(gsd)

add_subdirectory(CMake)
include(CFlagsSetup)

#############################################################################################
# Find libraries
include(PythonSetup)
include_directories(${PYTHON_INCLUDE_DIR})

#############################################################################################
# set the default install prefix
# option(INSTALL_USER "Install into python user site directory (like python setup.py install --user)" OFF)
# option(INSTALL_SITE "Install into python system site directory (like python setup.py install)" OFF)

# IF(INSTALL_USER)
#     SET(CMAKE_INSTALL_PREFIX ${PYTHON_USER_SITE} CACHE PATH "Python site installation directory" FORCE)
#     message(STATUS "Setting installation site dir: ${CMAKE_INSTALL_PREFIX}")
# ELSEIF(INSTALL_SITE)
if (INSTALL_SITE)
    SET(CMAKE_INSTALL_PREFIX ${PYTHON_SYSTEM_SITE} CACHE PATH "Python site installation directory" FORCE)
    message(STATUS "Setting installation site dir: ${CMAKE_INSTALL_PREFIX}")
ENDIF()

#############################################################################################
### Add project subdirs
include_directories(gsd)
add_subdirectory(gsd)
