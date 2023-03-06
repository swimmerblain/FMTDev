cmake_minimum_required(VERSION 3.0.2 FATAL_ERROR)
project(qbsofthand_industry_api_example VERSION 1.0.0 LANGUAGES CXX)

include_directories(include)
link_directories(libs)

# Build Settings
add_executable(${PROJECT_NAME}
  src/main.cpp
)

target_link_libraries(${PROJECT_NAME}
  PUBLIC
    qbsofthand_industry_api_x86
)

# C++ Settings
set_target_properties(
  ${PROJECT_NAME}
  PROPERTIES
    CXX_STANDARD 14
    CXX_STANDARD_REQUIRED ON
    COMPILE_FLAGS "-m32"
    LINK_FLAGS "-m32"
)

# Installation
install(
  TARGETS
    ${PROJECT_NAME}
  RUNTIME DESTINATION ${PROJECT_SOURCE_DIR}
)