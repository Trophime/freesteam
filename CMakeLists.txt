cmake_minimum_required(VERSION 3.2)

project(freesteam VERSION 2.2.1 )

set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules" ${CMAKE_MODULE_PATH})
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.h.in ${CMAKE_CURRENT_SOURCE_DIR}/config.h)

option( BUILD_TESTING "Build test" ON )
option( FREESTEAM_ENABLE_EXAMPLES "Enable examples" ON )
option( FREESTEAM_ENABLE_PYTHON "Enable Python Support" ON )

if (NOT FREESTEAM_PYTHON_VERSION)
  set(FREESTEAM_PYTHON_VERSION 3)
  MESSAGE(STATUS "Setting default PYTHON version to 3")
endif()

set(SRCS region1.c region2.c region3.c region4.c steam_ph.c
	steam.c backwards.c b23.c common.c derivs.c zeroin.c
	steam_ps.c solver2.c steam_pT.c steam_pu.c steam_Ts.c
	steam_Tx.c surftens.c
	bounds.c steam_pv.c viscosity.c thcond.c )

configure_file(config.h.in ${CMAKE_CURRENT_SOURCE_DIR}/config.h)

set(HEADERS backwards.h backwards_impl.h bounds.h common.h compat.h derivs.h region1.h region2.h region3.h region4.h solver2.h steam.h steam_ph.h steam_ps.h steam_pT.h steam_pu.h steam_pv.h steam_Ts.h steam_Tx.h steam_uv.h surftens.h thcond.h viscosity.h zeroin.h config.h)

find_package(gsl REQUIRED)
include_directories(${GSL_INCLUDES})
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# find_package(gtk2)
# find_package(ascend)

add_library( freesteam SHARED ${SRCS} )
set_target_properties( freesteam PROPERTIES VERSION ${PROJECT_VERSION} SOVERSION 2 )
target_link_libraries( freesteam m ${GSL_LIBRARIES})

# install
install( TARGETS freesteam DESTINATION ${INSTALL_LIB_DIR} ) #lib
install( FILES ${HEADERS} DESTINATION include/freesteam )

if (BUILD_TESTING)
  add_executable( mytest test.c )
  target_link_libraries( mytest  freesteam ${GSL_LIBRARIES})

  enable_testing()
  add_test(basic ${CMAKE_BINARY_DIR}/mytest)
endif()

if (FREESTEAM_EXAMPLES)
  add_subdirectory(examples)
endif()

# Add python bindings
if (FREESTEAM_ENABLE_PYTHON)
  FIND_PACKAGE(PythonInterp ${FREESTEAM_PYTHON_VERSION}  REQUIRED)
  if(PYTHONINTERP_FOUND)
    message(STATUS "[freesteam] Found python version ${PYTHON_VERSION}")
  else ()
    message(ERROR "[freesteam] No python version ${PYTHON_VERSION}")
  endif()
  FIND_PACKAGE(PythonLibs ${FREESTEAM_PYTHON_VERSION} REQUIRED)
  add_subdirectory(python)
endif()

