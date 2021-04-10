cmake_minimum_required(VERSION 3.14...3.20)

project(caesar LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Python3 REQUIRED COMPONENTS Development Interpreter)
find_package(pybind11 2.5 REQUIRED)
find_package(Eigen3 CONFIG REQUIRED)

set(CAESAR_PKGDIR
    "pkgs"
    CACHE STRING "Python package destination dir")


# the pure C++ library
add_library(caesar INTERFACE)
target_include_directories(
  caesar INTERFACE "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}>"
                   "$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>")
target_link_libraries(caesar INTERFACE Eigen3::Eigen)
add_library(caesar::caesar ALIAS caesar)
#install(TARGET caesar_extension LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}")

# the python bindings
pybind11_add_module(caesar_extension bindings/caesar.cpp)
target_link_libraries(caesar_extension PRIVATE caesar::caesar)
set_target_properties(caesar_extension PROPERTIES OUTPUT_NAME "caesar")
install(TARGETS caesar_extension DESTINATION "${CAESAR_PKGDIR}")
