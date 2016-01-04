cmake_minimum_required(VERSION 2.6.2 FATAL_ERROR)

if (CMAKE_MAJOR_VERSION VERSION_GREATER 2)
if(COMMAND cmake_policy)
    cmake_policy(SET CMP0042 OLD)
endif(COMMAND cmake_policy)
endif()

#########################################################################################
### Find Python and set PYTHON_SITEDIR, the location to install python modules
# macro for running python and getting output
macro(run_python code result)
execute_process(
    COMMAND
    ${PYTHON_EXECUTABLE} -c ${code}
    OUTPUT_VARIABLE ${result}
    RESULT_VARIABLE PY_ERR
    OUTPUT_STRIP_TRAILING_WHITESPACE
    )

if(PY_ERR)
    message(STATUS "Error while querying python for information")
endif(PY_ERR)
endmacro(run_python)

# find the python interpreter
find_program(PYTHON_EXECUTABLE NAMES python3 python)

# get the python installation prefix and version
run_python("import sys\; print('%d' % (sys.version_info[0]))" PYTHON_VERSION_MAJOR)
run_python("import sys\; print('%d' % (sys.version_info[1]))" PYTHON_VERSION_MINOR)
set(PYTHON_VERSION "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
string(REPLACE "." "" _python_version_no_dots ${PYTHON_VERSION})

# determine the include directory
if (PYTHON_VERSION VERSION_GREATER 3)
    run_python("import sysconfig\; print(sysconfig.get_path('include'))" _python_include_hint)
    run_python("import sysconfig\; print(sysconfig.get_config_var('LIBDIR'))" _python_lib_hint)
    run_python("import sysconfig\; print(sysconfig.get_config_var('LIBPL'))" _python_static_hint)

    if (ENABLE_STATIC)
        run_python("import sysconfig\; print(sysconfig.get_config_var('LIBRARY'))" _python_dynamic_lib_name)
    else()
        run_python("import sysconfig\; print(sysconfig.get_config_var('LDLIBRARY'))" _python_dynamic_lib_name)
    endif()
else()
    run_python("from distutils import sysconfig\; print sysconfig.get_python_inc()" _python_include_hint)
    run_python("from distutils import sysconfig\; print sysconfig.PREFIX" _python_prefix_hint)
    run_python("from distutils import sysconfig\; print sysconfig.get_config_var('LIBPL')" _python_static_hint)
    run_python("from distutils import sysconfig\; print sysconfig.get_config_var('LIBRARY')" _python_static_lib_name)
    run_python("from distutils import sysconfig\; print sysconfig.get_config_var('LDLIBRARY')" _python_dynamic_lib_name)
endif()

# always link the dynamic python library
get_filename_component(_python_lib_first ${_python_dynamic_lib_name} NAME)

find_path(PYTHON_INCLUDE_DIR Python.h
          HINTS ${_python_include_hint}
          NO_DEFAULT_PATH)

include_directories(${PYTHON_INCLUDE_DIR})

# determine the packages directory
run_python("from distutils import sysconfig\; print(sysconfig.get_python_lib( plat_specific=True))" _python_sitedir_absolute)
run_python("import sys\; print(sys.prefix)" _python_prefix)

# make packages directory relative to prefix
# string(REGEX MATCH "lib.*" PYTHON_SITEDIR ${_python_sitedir_absolute})
string(REPLACE "${_python_prefix}/" "" _python_sitedir_relative ${_python_sitedir_absolute})
set(PYTHON_SITEDIR ${_python_sitedir_relative} CACHE STRING "Python site-dir (relative to CMAKE_INSTALL_PREFIX)")

message(STATUS "Installing python modules into ${PYTHON_SITEDIR} in ${CMAKE_INSTALL_PREFIX}")

#############################################################################################
### Add project subdirs
include_directories(gsd)
add_subdirectory(gsd)
add_subdirectory(test)
install(DIRECTORY gsd DESTINATION ${PYTHON_SITEDIR})
