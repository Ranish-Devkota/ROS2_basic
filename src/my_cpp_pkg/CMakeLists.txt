cmake_minimum_required(VERSION 3.8)
project(my_cpp_pkg)

# #default to c++14
# if(NOT CMAKE_CXX_STANDARD)
#   set(CMAKE_CXX_STANDARD 14)
# endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

#WE CREATE EXECUTABLES
add_executable(cpp_node src/my_first_node.cpp) #name of executable is cpp_node
ament_target_dependencies(cpp_node rclcpp)

#WE INSTALL IT INSIDE PROJECT FILE
install(TARGETS
  cpp_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
