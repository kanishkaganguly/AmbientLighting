cmake_minimum_required(VERSION 3.5 FATAL_ERROR)
project(color_handler)
add_compile_options(-std=c++11)

add_subdirectory(external/pybind11)

find_package(pybind11 CONFIG)
if (pybind11_FOUND)
	message(STATUS "Pybind11 found")
	set(PYBIND11_PYTHON_VERSION 3.6)
else ()
	message(FATAL_ERROR "Pybind11 not found")
endif ()


find_package( OpenCV REQUIRED )
find_package(X11 REQUIRED)

set("COLOR_HANDLER_LIB" "color_handler")

include_directories(include ${pybind11_INCLUDE_DIRS}  ${OpenCV_INCLUDE_DIRS} ${X11_INCLUDE_DIR})

add_library(${COLOR_HANDLER_LIB} MODULE src/color_handler.cpp)
target_link_libraries(${COLOR_HANDLER_LIB} PRIVATE ${OpenCV_LIBS} ${X11_LIBRARIES} pybind11::module)

set_target_properties(${COLOR_HANDLER_LIB} PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/scripts")