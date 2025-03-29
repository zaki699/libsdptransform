cmake_minimum_required(VERSION 3.15)
project(sdptransform VERSION 1.2.10 LANGUAGES CXX)

#-----------------------------------------------------------------------------
# Options
#-----------------------------------------------------------------------------
option(SDPTRANSFORM_BUILD_TESTS "Build the test and readme-helper subdirs" ON)

#-----------------------------------------------------------------------------
# C++ Standard
#-----------------------------------------------------------------------------
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


# If old CMake or compilers:
add_compile_options(-std=c++14)

#-----------------------------------------------------------------------------
# Optional subdirectories (test, readme-helper)
#-----------------------------------------------------------------------------
if(SDPTRANSFORM_BUILD_TESTS)
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/test/CMakeLists.txt")
        add_subdirectory(test)
    endif()
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/readme-helper/CMakeLists.txt")
        add_subdirectory(readme-helper)
    endif()
endif()

#-----------------------------------------------------------------------------
# Library Sources/Headers
#-----------------------------------------------------------------------------
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include")

set(SDPTRANSFORM_SOURCE
    src/grammar.cpp
    src/parser.cpp
    src/writer.cpp
)

set(SDPTRANSFORM_HEADERS
    include/sdptransform.hpp
    include/json.hpp
)

#-----------------------------------------------------------------------------
# Build Library
#-----------------------------------------------------------------------------
add_library(sdptransform
    ${SDPTRANSFORM_SOURCE}
    ${SDPTRANSFORM_HEADERS}
)

# If user toggles BUILD_SHARED_LIBS to ON, this library will be shared;
# if OFF (default), it’s static..
target_include_directories(sdptransform
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

#-----------------------------------------------------------------------------
# Installation
#-----------------------------------------------------------------------------
# The library itself
install(TARGETS sdptransform
    EXPORT sdptransform-targets
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)
# The headers
install(FILES ${SDPTRANSFORM_HEADERS} DESTINATION include/sdptransform)

#-----------------------------------------------------------------------------
# CMake Config Files for find_package(sdptransform)
#-----------------------------------------------------------------------------
include(CMakePackageConfigHelpers)

write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/sdptransform-config-version.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

# A minimal sdptransform-config.cmake. 
file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/sdptransform-config.cmake" "
include(CMakeFindDependencyMacro)
# add any find_dependency(...) lines if needed
include(\"\${CMAKE_CURRENT_LIST_DIR}/sdptransform-targets.cmake\")
")

# Install config + version
install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/sdptransform-config.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/sdptransform-config-version.cmake"
    DESTINATION lib/cmake/sdptransform
)

# Export the library target
install(EXPORT sdptransform-targets
    FILE sdptransform-targets.cmake
    NAMESPACE sdptransform::
    DESTINATION lib/cmake/sdptransform
)

message(STATUS "sdptransform build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "BUILD_SHARED_LIBS=${BUILD_SHARED_LIBS}")
message(STATUS "SDPTRANSFORM_BUILD_TESTS=${SDPTRANSFORM_BUILD_TESTS}")