cmake_minimum_required(VERSION 3.10)
project(C++_Test)

aux_source_directory(src SRC_SUB)
aux_source_directory(. SRC_CUR)
add_executable(main ${SRC_SUB} ${SRC_CUR})
include_directories(include)
