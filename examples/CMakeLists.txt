include_directories(${CMAKE_CURRENT_SOURCE_DIR})

add-executable(isentropic isentropic.c)
target_link_libraries( test  freesteam ${GSL_LIBRARIES})
