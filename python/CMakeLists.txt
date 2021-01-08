cmake_policy(SET CMP0078 OLD)

find_package(SWIG )
if (SWIG_FOUND)
  INCLUDE(${SWIG_USE_FILE})

  if(NOT PYTHONLIBS_VERSION_STRING MATCHES "^2.*$" )
    set(CMAKE_SWIG_FLAGS -py3)
  endif()

  include_directories(${PYTHON_INCLUDE_DIRS})

  set(PYFREESTEAM_INSTALL_DIR ${CMAKE_INSTALL_PREFIX}/lib/python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}/dist-packages/)

  set (UseSWIG_TARGET_NAME_PREFERENCE LEGACY)
  set_property(SOURCE freesteam.i PROPERTY C ON)

  # swig_add_library(freesteam TYPE SHARED LANGUAGE python SOURCES freesteam.i)
  swig_add_library(freesteam LANGUAGE python SOURCES freesteam.i)

  # MESSAGE(STATUS "SWIG SWIG_MODULE_freesteam_REAL_NAME=${SWIG_MODULE_freesteam_REAL_NAME}")
  # MESSAGE(STATUS "GSL_LIBRARIES=${GSL_LIBRARIES}")

  #swig_link_libraries(freesteam freesteam ${GSL_LIBRARIES} ${PYTHON_LIBRARIES})
  set_property(TARGET ${SWIG_MODULE_freesteam_REAL_NAME} PROPERTY USE_TARGET_INCLUDE_DIRECTORIES TRUE)
  TARGET_LINK_LIBRARIES(${SWIG_MODULE_freesteam_REAL_NAME}  freesteam ${GSL_LIBRARIES} ${PYTHON_LIBRARIES})
  install(TARGETS ${SWIG_MODULE_freesteam_REAL_NAME} DESTINATION ${PYFREESTEAM_INSTALL_DIR})
  install(FILES ${CMAKE_BINARY_DIR}/python/freesteam.py DESTINATION ${PYFREESTEAM_INSTALL_DIR})

  enable_testing()
  add_test(test1 ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/test.py)
endif()
