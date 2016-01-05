############### cython based modules
add_library(fl SHARED gsd.c fl.c)
set_target_properties(fl PROPERTIES PREFIX "" OUTPUT_NAME "fl")
if(APPLE)
    set_target_properties(fl PROPERTIES SUFFIX ".so")
endif(APPLE)

################ Python only modules
# copy python modules to the build directory to make it a working python package
MACRO(copy_file file)
    ADD_CUSTOM_COMMAND (
        OUTPUT ${file}
        DEPENDS ${file}
        POST_BUILD
        COMMAND    ${CMAKE_COMMAND}
        ARGS       -E copy ${CMAKE_CURRENT_SOURCE_DIR}/${file} ${CMAKE_CURRENT_BINARY_DIR}/${file}
        COMMENT    "Copy gsd/${file}"
    )
ENDMACRO(copy_file)

set(files "__init__.py")

foreach(file ${files})
    copy_file(${file})
endforeach()

add_custom_target(copy_gsd ALL DEPENDS ${files})
