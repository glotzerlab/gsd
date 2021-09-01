# copy Python modules to the build directory to make it a working Python package
MACRO(copy_file file)
    add_custom_command (
        OUTPUT ${file}
        DEPENDS ${file}
        POST_BUILD
        COMMAND    ${CMAKE_COMMAND}
        ARGS       -E copy ${CMAKE_CURRENT_SOURCE_DIR}/${file} ${CMAKE_CURRENT_BINARY_DIR}/${file}
        COMMENT    "Copy gsd/test/${file}"
    )
ENDMACRO(copy_file)

set(files conftest.py pytest.ini test_fl.py test_gsd_v1.gsd test_hoomd.py test_largefile.py)

foreach(file ${files})
    copy_file(${file})
endforeach()

add_custom_target(copy_gsd_test ALL DEPENDS ${files})
