from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy
import os

class SdpTransformConan(ConanFile):
    name = "sdptransform"
    version = "1.2.10"
    license = "MIT"
    url = "https://github.com/zaki699/libsdptransform"
    description = "A C/C++ parser for SDP, with JSON logic from sdptransform"
    topics = ("webrtc", "sdp", "parser", "json")
    settings = "os", "arch", "compiler", "build_type"
    
    # We'll allow "shared" and "tests" as Conan options
    options = {
        "shared": [True, False],
        "tests": [True, False],
    }
    default_options = {
        "shared": False,
        "tests": False,
    }

    exports_sources = "CMakeLists.txt", "src/*", "include/*"

    # CMake package => a library
    package_type = "library"

    # For source():
    scm = {
        "type": "git",
        "url": "https://github.com/zaki699/libsdptransform.git",
        "revision": "main"
    }

    def layout(self):
        cmake_layout(self)

    def generate(self):
        # Create a CMake toolchain
        tc = CMakeToolchain(self)
        
        # If user wants a shared library, set BUILD_SHARED_LIBS=ON
        tc.variables["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        
        # If user wants to build tests, set SDPTRANSFORM_BUILD_TESTS=ON
        tc.variables["SDPTRANSFORM_BUILD_TESTS"] = "ON" if self.options.tests else "OFF"
        
        # If your library needs something else, set them here
        # e.g. tc.cache_variables["CMAKE_POSITION_INDEPENDENT_CODE"] = True if self.options.shared else ...
        
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # Run "cmake install"
        cmake = CMake(self)
        cmake.install()
        
        # Copy the license file from the source if available
        copy(self, "LICENSE", self.source_folder, 
             os.path.join(self.package_folder, "licenses"), keep_path=False)

    def package_info(self):
        # The library name is "sdptransform" as built by the CMakeLists
        self.cpp_info.libs = ["sdptransform"]
        
        self.cpp_info.set_property("cmake_file_name", "sdptransform")
        self.cpp_info.set_property("cmake_target_name", "sdptransform::sdptransform")
