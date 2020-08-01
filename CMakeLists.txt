cmake_minimum_required(VERSION 3.14 FATAL_ERROR) 
# By default, set the build type to Release
if(NOT DEFINED CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(default_build_type Release)
  message("Using default build type ${default_build_type}")
  set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
    STRING "Select build type" FORCE
  )
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY
    STRINGS "" Debug Release MinSizeRel RelWithDebInfo
  )
endif()

project(leptoneff CXX)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/lib")

# Require C++17 in all targets
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_compile_options(-Wall -Wextra -pedantic)

# Find external dependencies
find_package(ROOT 6 REQUIRED)
find_package(yaml-cpp REQUIRED DEBUG)



add_library(leptoneff SHARED
  src/Ntuple.cc
	src/ArgParser.cc
	src/SmartSelectionMonitor.cc
)
target_include_directories(leptoneff PUBLIC include)
target_link_libraries(leptoneff
  PUBLIC ROOT::Hist ROOT::MathCore ROOT::Physics ROOT::Tree ROOT::TreePlayer
  PUBLIC yaml-cpp
)

add_executable(example_ntuple src/example_ntuple.cc)
target_link_libraries(example_ntuple PRIVATE leptoneff)
add_executable(test src/test.cc)
target_link_libraries(test PRIVATE leptoneff)

