cmake_minimum_required(VERSION 3.5)

project(boba-cup-checker LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(boba-cup-checker main.cpp ColorFinder.cpp ColorFinder.h CamManager.cpp CamManager.h VisionCommon.h)

set(OpenCV_DIR [OpenCV.cmake PATH])
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIR})
target_link_libraries(boba-cup-checker ${OpenCV_LIBRARIES})


