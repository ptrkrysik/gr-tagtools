INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_TAGTOOLS tagtools)

FIND_PATH(
    TAGTOOLS_INCLUDE_DIRS
    NAMES tagtools/api.h
    HINTS $ENV{TAGTOOLS_DIR}/include
        ${PC_TAGTOOLS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    TAGTOOLS_LIBRARIES
    NAMES gnuradio-tagtools
    HINTS $ENV{TAGTOOLS_DIR}/lib
        ${PC_TAGTOOLS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(TAGTOOLS DEFAULT_MSG TAGTOOLS_LIBRARIES TAGTOOLS_INCLUDE_DIRS)
MARK_AS_ADVANCED(TAGTOOLS_LIBRARIES TAGTOOLS_INCLUDE_DIRS)

