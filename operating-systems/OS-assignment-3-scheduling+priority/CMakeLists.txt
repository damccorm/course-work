cmake_minimum_required(VERSION 2.8)
project (Assignment1)
enable_testing()
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x -g")
add_executable (shell main.cpp app.cpp utilities.cpp)
add_test(NAME correctExecution
COMMAND ${PROJECT_SOURCE_DIR}/test-correct-execution.sh
WORKING_DIRECTORY ${PROJECT_SOURCE_DIR})


