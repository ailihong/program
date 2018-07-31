cmake_minimum_required (VERSION 2.8)  
      
project (test)  

add_executable(test test.cpp sqlite_db.cpp)

include_directories(${PROJECT_SOURCE_DIR})
include_directories (
        /usr/local/include  
        /usr/include 
        )
target_link_libraries(test  
        /usr/lib/x86_64-linux-gnu/libsqlite3.so
        )
