include(FindPackageMessage)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# http://www.mariobadr.com/using-clang-tidy-with-cmake-36.html
find_program(
  CLANG_TIDY_EXE
  NAMES "clang-tidy"
  DOC "Path to clang-tidy executable"
  )
if(CLANG_TIDY_EXE)
find_package_message(CLANG_TIDY "Found clang-tidy: ${CLANG_TIDY_EXE}" "[${CLANG_TIDY_EXE}]")
set(DO_CLANG_TIDY "${CLANG_TIDY_EXE}" "-p=${CMAKE_BINARY_DIR}" "-header-filter=^${CMAKE_SOURCE_DIR}/.*")
endif()
