add_library(gsd SHARED gsd.c)
set_target_properties(gsd PROPERTIES SOVERSION 1)
set_target_properties(gsd PROPERTIES VERSION "0.0")

install(TARGETS gsd
        LIBRARY DESTINATION lib)
install(FILES gsd.h DESTINATION include)

