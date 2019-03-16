cmake_minimum_required(VERSION 2.8)
project (assignment-4)
enable_testing()
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --std=c++11 -g")
include_directories(${CMAKE_SOURCE_DIR} ${CMAKE_SOURCE_DIR}/library)

add_library(taskhelper ${CMAKE_SOURCE_DIR}/library/task.cpp)
target_link_libraries (taskhelper pthread rt)

add_executable(taskexample main.cpp server.cpp client.cpp container.cpp)
target_link_libraries (taskexample taskhelper)

add_test(NAME correctExecution
COMMAND ${PROJECT_SOURCE_DIR}/test.sh
WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})
