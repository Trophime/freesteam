# - Find GSL
# Find the native GSL includes and library
# You can specify these variables to search
#
#  GSL_DIR
#
# The module provides these variables:
#
#  GSL_INCLUDES_DIRS - where to find headers.
#  GSL_LIBRARY_DIRS  - where to find libraries
#  GSL_LIBRARIES     - List of libraries when using GSL.
#  GSL_FOUND         - True if GSL found.


find_path (GSL_INCLUDE_DIRS NAMES gsl/gsl_math.h
    HINTS $ENV{GSL_DIR}/include ${GSL_DIR}/include
)

find_library (GSL_LIBRARY NAME gsl
    HINTS $ENV{GSL_DIR}/lib ${GSL_DIR}/lib
)
SET(GSL_LIBRARIES "${GSL_LIBRARY}")

find_library (GSL_CBLAS_LIBRARY NAMES gslcblas
    HINTS $ENV{GSL_DIR}/lib ${GSL_DIR}/lib
)
LIST( APPEND GSL_LIBRARIES "${GSL_CBLAS_LIBRARY}")
MESSAGE(STATUS "GSL_LIBRARIES=${GSL_LIBRARIES}")
set( GSL_LIBRARIES ${GSL_LIBRARIES} CACHE INTERNAL "")

# # check gsl_cadna.h to active cadna support
# find_path (GSL_CADNA_INCLUDE_DIRS NAMES gsl/gsl_cadna.h
#     HINTS $ENV{GSL_DIR}/include ${GSL_DIR}/include
# )
# if (GSL_CADNA_INCLUDE_DIRS)
#   MESSAGE(STATUS "gsl is build with cadna support")
#   add_definitions(-DGSL_HAS_CADNA)

#   # TODO: should add cadna to library
#   Find_package(Cadna)
# endif()


set( GSL_LIBRARY_DIRS "")
foreach( LIB ${GSL_LIBRARIES} )
    get_filename_component( DIR "${LIB}" DIRECTORY )
    list( APPEND GSL_LIBRARY_DIRS "${DIR}" )
    MESSAGE(STATUS "LIB=${LIB}")
endforeach()
list( REMOVE_DUPLICATES GSL_LIBRARY_DIRS )
set( GSL_LIBRARY_DIRS ${GSL_LIBRARY_DIRS} CACHE INTERNAL "")

# Backward compat
set( GSL_LIB ${GSL_LIBRARIES} )
set( GSL_INCLUDES "${GSL_INCLUDE_DIRS}" )

include (FindPackageHandleStandardArgs)
find_package_handle_standard_args(GSL REQUIRED_VARS GSL_LIBRARIES GSL_INCLUDE_DIRS GSL_LIBRARY_DIRS GSL_INCLUDES GSL_LIB)
