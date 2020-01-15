add_executable(benchmark-write benchmark-write.cc ../gsd/gsd.c)
set_property(TARGET benchmark-write PROPERTY CXX_STANDARD 11)
add_executable(benchmark-read benchmark-read.cc ../gsd/gsd.c)
set_property(TARGET benchmark-read PROPERTY CXX_STANDARD 11)
