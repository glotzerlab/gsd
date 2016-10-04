############### cython based modules

if (CYTHON_EXECUTABLE)
    add_custom_command (
        OUTPUT fl.c
        DEPENDS fl.pyx libgsd.pxd
        COMMAND    ${CYTHON_EXECUTABLE}
        ARGS       -${PYTHON_VERSION_MAJOR} -I ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/fl.pyx -o ${CMAKE_CURRENT_BINARY_DIR}/fl.c
        COMMENT    "Cythonizing fl.pyx"
    )

    set(FL_SRC fl.c)
else()
    file(READ "fl.pyx.sha256" __input)
    string(STRIP ${__input} __original_hash)
    file(SHA256 "${CMAKE_CURRENT_SOURCE_DIR}/fl.pyx" __current_hash)

    if ("${__current_hash}" STREQUAL "${__original_hash}")
        set(FL_SRC "fl${PYTHON_VERSION_MAJOR}.c")
    else()
        message(SEND_ERROR "fl.pyx updated, embedded c files out of date. Build with cython enabled.")
    endif()
endif()

set_source_files_properties(${FL_SRC} PROPERTIES COMPILE_DEFINITIONS NO_IMPORT_ARRAY)

add_library(fl SHARED gsd.c ${FL_SRC})

set_target_properties(fl PROPERTIES PREFIX "" OUTPUT_NAME "fl" MACOSX_RPATH "On")
if(APPLE)
    set_target_properties(fl PROPERTIES SUFFIX ".so")
    target_link_libraries(fl ${PYTHON_LIBRARY})
    fix_conda_python(fl)
endif(APPLE)

if (WIN32)
    target_link_libraries(fl ${PYTHON_LIBRARY})
    set_target_properties(fl PROPERTIES SUFFIX ".pyd")
endif()

################ Python only modules
# copy python modules to the build directory to make it a working python package
MACRO(copy_file file)
    add_custom_command (
        OUTPUT ${file}
        DEPENDS ${file}
        POST_BUILD
        COMMAND    ${CMAKE_COMMAND}
        ARGS       -E copy ${CMAKE_CURRENT_SOURCE_DIR}/${file} ${CMAKE_CURRENT_BINARY_DIR}/${file}
        COMMENT    "Copy gsd/${file}"
    )
ENDMACRO(copy_file)

set(files __init__.py hoomd.py pygsd.py)

foreach(file ${files})
    copy_file(${file})
endforeach()

add_custom_target(copy_gsd ALL DEPENDS ${files})

if (NOT WIN32)

install(TARGETS fl
        LIBRARY DESTINATION ${PYTHON_MODULE_BASE_DIR}
        )

install(FILES ${files}
        DESTINATION ${PYTHON_MODULE_BASE_DIR}
       )

endif()
