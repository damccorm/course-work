# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/vagrant/projects/assignment-5-dannymccormick3

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/vagrant/projects/assignment-5-dannymccormick3/build

# Include any dependencies generated for this target.
include CMakeFiles/taskexample.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/taskexample.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/taskexample.dir/flags.make

CMakeFiles/taskexample.dir/main.cpp.o: CMakeFiles/taskexample.dir/flags.make
CMakeFiles/taskexample.dir/main.cpp.o: ../main.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/vagrant/projects/assignment-5-dannymccormick3/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/taskexample.dir/main.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/taskexample.dir/main.cpp.o -c /home/vagrant/projects/assignment-5-dannymccormick3/main.cpp

CMakeFiles/taskexample.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/taskexample.dir/main.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/vagrant/projects/assignment-5-dannymccormick3/main.cpp > CMakeFiles/taskexample.dir/main.cpp.i

CMakeFiles/taskexample.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/taskexample.dir/main.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/vagrant/projects/assignment-5-dannymccormick3/main.cpp -o CMakeFiles/taskexample.dir/main.cpp.s

CMakeFiles/taskexample.dir/main.cpp.o.requires:
.PHONY : CMakeFiles/taskexample.dir/main.cpp.o.requires

CMakeFiles/taskexample.dir/main.cpp.o.provides: CMakeFiles/taskexample.dir/main.cpp.o.requires
	$(MAKE) -f CMakeFiles/taskexample.dir/build.make CMakeFiles/taskexample.dir/main.cpp.o.provides.build
.PHONY : CMakeFiles/taskexample.dir/main.cpp.o.provides

CMakeFiles/taskexample.dir/main.cpp.o.provides.build: CMakeFiles/taskexample.dir/main.cpp.o

CMakeFiles/taskexample.dir/server.cpp.o: CMakeFiles/taskexample.dir/flags.make
CMakeFiles/taskexample.dir/server.cpp.o: ../server.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/vagrant/projects/assignment-5-dannymccormick3/build/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/taskexample.dir/server.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/taskexample.dir/server.cpp.o -c /home/vagrant/projects/assignment-5-dannymccormick3/server.cpp

CMakeFiles/taskexample.dir/server.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/taskexample.dir/server.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/vagrant/projects/assignment-5-dannymccormick3/server.cpp > CMakeFiles/taskexample.dir/server.cpp.i

CMakeFiles/taskexample.dir/server.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/taskexample.dir/server.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/vagrant/projects/assignment-5-dannymccormick3/server.cpp -o CMakeFiles/taskexample.dir/server.cpp.s

CMakeFiles/taskexample.dir/server.cpp.o.requires:
.PHONY : CMakeFiles/taskexample.dir/server.cpp.o.requires

CMakeFiles/taskexample.dir/server.cpp.o.provides: CMakeFiles/taskexample.dir/server.cpp.o.requires
	$(MAKE) -f CMakeFiles/taskexample.dir/build.make CMakeFiles/taskexample.dir/server.cpp.o.provides.build
.PHONY : CMakeFiles/taskexample.dir/server.cpp.o.provides

CMakeFiles/taskexample.dir/server.cpp.o.provides.build: CMakeFiles/taskexample.dir/server.cpp.o

CMakeFiles/taskexample.dir/client.cpp.o: CMakeFiles/taskexample.dir/flags.make
CMakeFiles/taskexample.dir/client.cpp.o: ../client.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/vagrant/projects/assignment-5-dannymccormick3/build/CMakeFiles $(CMAKE_PROGRESS_3)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/taskexample.dir/client.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/taskexample.dir/client.cpp.o -c /home/vagrant/projects/assignment-5-dannymccormick3/client.cpp

CMakeFiles/taskexample.dir/client.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/taskexample.dir/client.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/vagrant/projects/assignment-5-dannymccormick3/client.cpp > CMakeFiles/taskexample.dir/client.cpp.i

CMakeFiles/taskexample.dir/client.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/taskexample.dir/client.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/vagrant/projects/assignment-5-dannymccormick3/client.cpp -o CMakeFiles/taskexample.dir/client.cpp.s

CMakeFiles/taskexample.dir/client.cpp.o.requires:
.PHONY : CMakeFiles/taskexample.dir/client.cpp.o.requires

CMakeFiles/taskexample.dir/client.cpp.o.provides: CMakeFiles/taskexample.dir/client.cpp.o.requires
	$(MAKE) -f CMakeFiles/taskexample.dir/build.make CMakeFiles/taskexample.dir/client.cpp.o.provides.build
.PHONY : CMakeFiles/taskexample.dir/client.cpp.o.provides

CMakeFiles/taskexample.dir/client.cpp.o.provides.build: CMakeFiles/taskexample.dir/client.cpp.o

CMakeFiles/taskexample.dir/container.cpp.o: CMakeFiles/taskexample.dir/flags.make
CMakeFiles/taskexample.dir/container.cpp.o: ../container.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/vagrant/projects/assignment-5-dannymccormick3/build/CMakeFiles $(CMAKE_PROGRESS_4)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/taskexample.dir/container.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/taskexample.dir/container.cpp.o -c /home/vagrant/projects/assignment-5-dannymccormick3/container.cpp

CMakeFiles/taskexample.dir/container.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/taskexample.dir/container.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/vagrant/projects/assignment-5-dannymccormick3/container.cpp > CMakeFiles/taskexample.dir/container.cpp.i

CMakeFiles/taskexample.dir/container.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/taskexample.dir/container.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/vagrant/projects/assignment-5-dannymccormick3/container.cpp -o CMakeFiles/taskexample.dir/container.cpp.s

CMakeFiles/taskexample.dir/container.cpp.o.requires:
.PHONY : CMakeFiles/taskexample.dir/container.cpp.o.requires

CMakeFiles/taskexample.dir/container.cpp.o.provides: CMakeFiles/taskexample.dir/container.cpp.o.requires
	$(MAKE) -f CMakeFiles/taskexample.dir/build.make CMakeFiles/taskexample.dir/container.cpp.o.provides.build
.PHONY : CMakeFiles/taskexample.dir/container.cpp.o.provides

CMakeFiles/taskexample.dir/container.cpp.o.provides.build: CMakeFiles/taskexample.dir/container.cpp.o

# Object files for target taskexample
taskexample_OBJECTS = \
"CMakeFiles/taskexample.dir/main.cpp.o" \
"CMakeFiles/taskexample.dir/server.cpp.o" \
"CMakeFiles/taskexample.dir/client.cpp.o" \
"CMakeFiles/taskexample.dir/container.cpp.o"

# External object files for target taskexample
taskexample_EXTERNAL_OBJECTS =

taskexample: CMakeFiles/taskexample.dir/main.cpp.o
taskexample: CMakeFiles/taskexample.dir/server.cpp.o
taskexample: CMakeFiles/taskexample.dir/client.cpp.o
taskexample: CMakeFiles/taskexample.dir/container.cpp.o
taskexample: CMakeFiles/taskexample.dir/build.make
taskexample: libtaskhelper.a
taskexample: CMakeFiles/taskexample.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX executable taskexample"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/taskexample.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/taskexample.dir/build: taskexample
.PHONY : CMakeFiles/taskexample.dir/build

CMakeFiles/taskexample.dir/requires: CMakeFiles/taskexample.dir/main.cpp.o.requires
CMakeFiles/taskexample.dir/requires: CMakeFiles/taskexample.dir/server.cpp.o.requires
CMakeFiles/taskexample.dir/requires: CMakeFiles/taskexample.dir/client.cpp.o.requires
CMakeFiles/taskexample.dir/requires: CMakeFiles/taskexample.dir/container.cpp.o.requires
.PHONY : CMakeFiles/taskexample.dir/requires

CMakeFiles/taskexample.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/taskexample.dir/cmake_clean.cmake
.PHONY : CMakeFiles/taskexample.dir/clean

CMakeFiles/taskexample.dir/depend:
	cd /home/vagrant/projects/assignment-5-dannymccormick3/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/vagrant/projects/assignment-5-dannymccormick3 /home/vagrant/projects/assignment-5-dannymccormick3 /home/vagrant/projects/assignment-5-dannymccormick3/build /home/vagrant/projects/assignment-5-dannymccormick3/build /home/vagrant/projects/assignment-5-dannymccormick3/build/CMakeFiles/taskexample.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/taskexample.dir/depend
