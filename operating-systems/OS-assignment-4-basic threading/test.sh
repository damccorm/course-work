#!/bin/sh


#Running the Program
execute() {
        set -e
	a=$(./build/taskexample)
        echo "Output: " $a
}

execute

