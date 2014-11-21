add_executable(test_write test_write.cc)
target_link_libraries(test_write gsd)

add_executable(test_read test_read.cc)
target_link_libraries(test_read gsd)
