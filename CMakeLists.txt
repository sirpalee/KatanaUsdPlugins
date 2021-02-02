# Modifications Copyright 2020 Autodesk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
cmake_minimum_required(VERSION 3.12)
project(KatanaUsdPlugins)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
                      ${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules
                      ${CMAKE_CURRENT_SOURCE_DIR}/cmake/macros)

#Set default option value in case PXR_PY_PACKAGE_NAME is not defined
set(PXR_PY_PACKAGE_NAME "pxr"
    CACHE
    STRING
    "Name for the root python bindings package"
)

# Ensure we can get the root of this project at all times.
set(KATANA_USD_PLUGINS_SRC_ROOT ${CMAKE_CURRENT_SOURCE_DIR})
include(Support)
if(NOT GEOLIB_API_SOURCE_DIR)
    set(GEOLIB_API_SOURCE_DIR ${KATANA_API_SOURCE_DIR})
endif()

message(STATUS "KATANA_API_SOURCE_DIR is ${KATANA_API_SOURCE_DIR}")
message(STATUS "GEOLIB_API_SOURCE_DIR is ${GEOLIB_API_SOURCE_DIR}")

option(ENABLE_USD_EXPORT "Enables building and installing the \
    UsdExport subdirectory and supporting logic." ON)

option(ENABLE_USD_RENDER_INFO_PLUGIN "Enables building and installing the \
    UsdRenderInfoPlugin subdirectory and supporting logic." ON)

add_subdirectory(lib)
add_subdirectory(plugin)
add_subdirectory(python)

install(FILES LICENSE.txt
        DESTINATION .)

install(FILES NOTICE.txt
        DESTINATION .)
