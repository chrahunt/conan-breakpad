project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Minimum required for breakpad.
set(CMAKE_CXX_STANDARD 11)

add_executable(example example.cpp)
target_link_libraries(example ${CONAN_LIBS})
