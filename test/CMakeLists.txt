add_executable(test_write test_write.cc ${CMAKE_SOURCE_DIR}/gsd/gsd_mmap.c)
target_link_libraries(test_write)

add_executable(test_read test_read.cc ${CMAKE_SOURCE_DIR}/gsd/gsd_mmap.c)
target_link_libraries(test_read)
