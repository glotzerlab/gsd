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
if (NOT PYTHON_SITEDIR)
    find_program(PYTHON_EXECUTABLE NAMES python3 python)
endif()
find_package(PythonInterp REQUIRED)

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
include_directories(libgsd)
add_subdirectory(libgsd)
add_subdirectory(test)

install(DIRECTORY gsd DESTINATION ${PYTHON_SITEDIR})
