cmake_minimum_required(VERSION 3.10)  # Specify the minimum version of CMake.

project(FlashExperiment)  # Name your project.


#  Add the onnxruntime library to the project.
find_path(ONNX_RUNTIME_SESSION_INCLUDE_DIRS onnxruntime_cxx_api.h HINTS /usr/local/include/onnxruntime/core/session/)
find_library(ONNX_RUNTIME_LIB onnxruntime HINTS /usr/local/lib)


# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add include directories
include_directories(include)



# Add source directory
add_executable(FlashExperiment src/main.cpp)
target_include_directories(onnx_c++ PRIVATE ${ONNX_RUNTIME_SESSION_INCLUDE_DIRS} ${OpenCV_INCLUDE_DIRS})
target_link_libraries(onnx_c++ PRIVATE ${ONNX_RUNTIME_LIB} ${OpenCV_LIBRARIES})

# If you have additional libraries to link:
# target_link_libraries(FlashExperiment name_of_library)
