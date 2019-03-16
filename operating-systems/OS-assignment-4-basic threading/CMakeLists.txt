cmake_minimum_required(VERSION 2.8)
project (assignment-4)
enable_testing()
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --std=c++11 -g")
include_directories("${CMAKE_SOURCE_DIR}")

add_library(taskhelper task.cpp)
target_link_libraries (taskhelper pthread rt)

add_executable(taskexample example.cpp)
target_link_libraries (taskexample taskhelper)

add_test(NAME correctExecution
COMMAND ${PROJECT_SOURCE_DIR}/test.sh
WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})
