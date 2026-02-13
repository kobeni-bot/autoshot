cmake_minimum_required(VERSION 3.10)
project(autoshot_cpp)

set(CMAKE_CXX_STANDARD 17)

# Find required packages
find_package(OpenCV REQUIRED)

# Include directories
include_directories(include)

# Source files
set(SOURCES
    src/main.cpp
    src/window_manager.cpp
    src/image_processor.cpp
    src/similarity_detector.cpp
    src/utils.cpp
)

# Header files
set(HEADERS
    include/window_manager.h
    include/image_processor.h
    include/similarity_detector.h
    include/utils.h
)

# Executable
add_executable(autoshot_cpp ${SOURCES} ${HEADERS})

# Link libraries
target_link_libraries(autoshot_cpp ${OpenCV_LIBS} gdi32 user32)

# Set output directory
set_target_properties(autoshot_cpp PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)