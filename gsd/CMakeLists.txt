add_library(file SHARED gsd.c file.c)
set_target_properties(file PROPERTIES SOVERSION 1)
set_target_properties(file PROPERTIES VERSION "0.0")

# tweak the properties of the output to make a functional python module
set_target_properties(file PROPERTIES PREFIX "" OUTPUT_NAME "file")

# .dylib is not regognized as a python module by python on Mac OS X
if(APPLE)
    set_target_properties(file PROPERTIES SUFFIX ".so")
endif(APPLE)
