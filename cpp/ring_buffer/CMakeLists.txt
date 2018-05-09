cmake_minimum_required(VERSION 2.8)

set(CMAKE_CXX_FLAGS -std=c++11)

include_directories(${PROJECT_SOURCE_DIR})

set(src_file
${PROJECT_SOURCE_DIR}/ring_buffer.cpp
${PROJECT_SOURCE_DIR}/test.cpp
)

add_executable(test ${src_file})

target_link_libraries(test pthread)

