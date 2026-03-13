cmake_minimum_required(VERSION 3.5)
project(Simulation)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# Find Geant4
find_package(Geant4 REQUIRED ui_all vis_all)
include(${Geant4_USE_FILE})
# ===== Source files =====
file(GLOB SRC_FILES CONFIGURE_DEPENDS
    ${PROJECT_SOURCE_DIR}/src/*.cc
)
set(MAIN_FILE
    ${PROJECT_SOURCE_DIR}/sim.cc
)
# ===== executable files =====
add_executable(sim
    ${MAIN_FILE}
    ${SRC_FILES}
)
# ===== head files =====
target_include_directories(sim PRIVATE
    ${PROJECT_SOURCE_DIR}/include
)
# ===== link Geant4 =====
target_link_libraries(sim
    ${Geant4_LIBRARIES}
)
# ===== copy macro files =====
file(GLOB MACRO_FILES CONFIGURE_DEPENDS
    ${PROJECT_SOURCE_DIR}/*.mac
)
file(COPY ${MACRO_FILES} DESTINATION ${PROJECT_BINARY_DIR})
add_custom_target(Simulation DEPENDS sim)