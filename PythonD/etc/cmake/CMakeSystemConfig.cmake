# 
# CMakeLocal.make.in should be in the directory where you run configure
# in, which need not be the source directory
#
SET (CMAKE_WORDS_BIGENDIAN    )

SET (CMAKE_USE_SPROC          0 CACHE BOOL 
     "Use sproc libs.")

SET (CMAKE_USE_PTHREADS       1 CACHE BOOL
     "Use the pthreads library.")

IF(WIN32)
  SET (CMAKE_USE_WIN32_THREADS   CACHE BOOL
       "Use the win32 thread library.")
ENDIF(WIN32)

SET (CMAKE_HP_PTHREADS        0 CACHE BOOL
     "Use HP pthreads.")

SET (CMAKE_LIB_EXT             CACHE STRING
     "Library extension used by this machine.")

SET (CMAKE_RANLIB             "ranlib" CACHE FILEPATH 
     "Library randomizer program used on archive libraries.")

SET (CMAKE_AR                 "/dev/d/user/djgpp/bin/ar" CACHE FILEPATH 
     "Archive program used to make archive libraries.")

SET (CMAKE_AR_ARGS            "cr" CACHE STRING 
     "Arguments for CMAKE_AR program to create an archive library.")

SET (CMAKE_CXX_COMPILER       "gpp" CACHE FILEPATH 
     "Name of C++ compiler used.")

SET (CMAKE_CXX_FLAGS          "-g -O2" CACHE STRING 
     "Flags used by CXX compiler.")

SET (CMAKE_TEMPLATE_FLAGS     "" CACHE STRING
     "CXX template flags used by compiler.")

SET (CMAKE_C_COMPILER         "gcc" CACHE FILEPATH
     "Name of C compiler used.")

SET (CMAKE_C_FLAGS            "-g -O2" CACHE STRING 
     "Flags for C compiler.")

SET (CMAKE_SHLIB_CFLAGS       "-fPIC" CACHE STRING
     "Flag used for building shared library objects.")

SET (CMAKE_SHLIB_BUILD_FLAGS  "" CACHE STRING
     "Flag used by CXX to build a shared library.")

SET (CMAKE_MODULE_BUILD_FLAGS "" CACHE STRING
     "Flag used by CXX to build a shared library.")

SET (CMAKE_INSTALL_PREFIX     /dev/env/DJDIR CACHE PATH 
     "Install path prefix, prepended onto install directories.")

SET (CMAKE_SHLIB_SUFFIX        CACHE STRING 
     "Shared library suffix.")

SET (CMAKE_MODULE_SUFFIX       CACHE STRING 
     "Module library suffix.")

SET (CMAKE_THREAD_LIBS        "" CACHE STRING
     "Thread library used.")

SET (CMAKE_DL_LIBS            "" CACHE STRING 
     "Dynamic link library to link in.")

SET (CMAKE_SHLIB_LINK_FLAGS   "" CACHE STRING
     "Flags used to link a shared library.")

SET (CMAKE_MODULE_LINK_FLAGS  "" CACHE STRING
     "Flags used to link a shared library.")

SET (CMAKE_SHLIB_LD_LIBS      "" CACHE STRING 
     "Libraries used by LD for shared libraries.")

SET (CMAKE_SHLIB_RUNTIME_FLAG "" CACHE STRING
     "Flag used to specify run-time search paths.")

SET (CMAKE_SHLIB_RUNTIME_SEP "" CACHE STRING
     "If null, each runtime path is a separate option. Otherwise, they are all joined, separated by this.")

SET (CMAKE_SKIP_RPATH "NO" CACHE BOOL
     "If set, runtime paths are not added when using shared libraries.")

# support for X11

SET (CMAKE_X_LIBS             "  -lX11 -lXext " CACHE STRING 
     "Libraries and options used in X11 programs.")

SET (CMAKE_X_CFLAGS           "" CACHE STRING 
     "X11 extra flags.")

SET (CMAKE_HAS_X              0 CACHE INTERNAL 
     "Is X11 around.")

SET (CMAKE_NO_ANSI_STREAM_HEADERS  CACHE INTERNAL 
     "Does the compiler support headers like iostream.")

SET (CMAKE_NO_STD_NAMESPACE     CACHE INTERNAL 
     "Does the compiler support std::.")

SET (CMAKE_NO_ANSI_FOR_SCOPE    CACHE INTERNAL 
     "Does the compiler support ansi for scoping.")

SET (CMAKE_COMPILER_IS_GNUCXX 1 CACHE INTERNAL 
     "Is the compile GNU C++.")

SET (CMAKE_ANSI_CFLAGS         CACHE INTERNAL 
     "What flags are required by the c++ compiler to make it ansi.")

SET (CMAKE_ANSI_CXXFLAGS       CACHE INTERNAL 
     "What flags are required by the c++ compiler to make it ansi.")

SET (CMAKE_NO_EXPLICIT_TEMPLATE_INSTANTIATION         CACHE INTERNAL 
     "Does the compiler not support explicit template instantiation.")

SET (CMAKE_SIZEOF_INT       4   CACHE INTERNAL "Size of int data type")
SET (CMAKE_SIZEOF_LONG      4   CACHE INTERNAL "Size of long data type")
SET (CMAKE_SIZEOF_VOID_P    4  CACHE INTERNAL "Size of void* data type")
SET (CMAKE_SIZEOF_CHAR      1  CACHE INTERNAL "Size of char data type")
SET (CMAKE_SIZEOF_SHORT     2  CACHE INTERNAL "Size of short data type")
SET (CMAKE_SIZEOF_FLOAT     4  CACHE INTERNAL "Size of float data type")
SET (CMAKE_SIZEOF_DOUBLE    8  CACHE INTERNAL "Size of double data type")

FIND_PROGRAM(CMAKE_MAKE_PROGRAM NAMES gmake make )

# The following variables are advanced 

MARK_AS_ADVANCED(
CMAKE_X_LIBS
CMAKE_USE_WIN32_THREADS
CMAKE_USE_SPROC
CMAKE_USE_PTHREADS
CMAKE_OBJECT_FILE_SUFFIX
CMAKE_EXECUTABLE_SUFFIX
CMAKE_STATICLIB_SUFFIX
CMAKE_SHLIB_SUFFIX
CMAKE_MODULE_SUFFIX
CMAKE_CXX_COMPILER
CMAKE_C_COMPILER
CMAKE_HP_PTHREADS
CMAKE_WORDS_BIGENDIAN
CMAKE_LIB_EXT
CMAKE_RANLIB
CMAKE_AR
CMAKE_AR_ARGS
CMAKE_TEMPLATE_FLAGS
CMAKE_SHLIB_CFLAGS
CMAKE_SHLIB_BUILD_FLAGS
CMAKE_MODULE_BUILD_FLAGS
CMAKE_THREAD_LIBS
CMAKE_DL_LIBS
CMAKE_SHLIB_LINK_FLAGS
CMAKE_MODULE_LINK_FLAGS
CMAKE_SHLIB_LD_LIBS
CMAKE_SHLIB_RUNTIME_FLAG
CMAKE_SHLIB_RUNTIME_SEP
CMAKE_SKIP_RPATH
CMAKE_X_CFLAGS
CMAKE_NO_ANSI_STREAM_HEADERS
CMAKE_NO_ANSI_FOR_SCOPE
CMAKE_NO_STD_NAMESPACE
CMAKE_COMPILER_IS_GNUCXX
CMAKE_ANSI_CFLAGS
CMAKE_ANSI_CXXFLAGS
CMAKE_NO_EXPLICIT_TEMPLATE_INSTANTIATION
CMAKE_MAKE_PROGRAM
)
