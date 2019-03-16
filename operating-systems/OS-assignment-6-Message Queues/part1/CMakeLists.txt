project(mq_example)
add_executable(mqueue_r mqueue_r.cpp)
add_executable(mqueue_s mqueue_s.cpp)
target_link_libraries(mqueue_r rt)
target_link_libraries(mqueue_s rt)

