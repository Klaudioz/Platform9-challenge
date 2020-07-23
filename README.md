## How to run it
Install: `pip3 install -r requirements.txt`

Run it:  `python 3 dependencies_list.py`

Test it: `python 3 test_dependencies_list.py`

All the documentation is inside the code.

## Description

Assume you have a set of python functions that depend on one another in a directed graph, similar to a makefile conceptually. For example — 

- function A - depends on nothing - prints “result of function A”

- function B - depends on function A - prints “result of function B”

- function C - depends on function A - prints “result of function C”

- function D - depends on function B and C - prints “result of function D”

- function E - depends on function B - prints “result of function E”

- function F - depends on function D and function E - prints “result of function F”

Functions A to F are just examples, there could be any number of functions to handle with any number of functions they depend on.
Design and implement a program in python that allows a user to choose a ‘target’ function from the graph, and run it. Your graph may be stored in a static dependency file, in any format of your choice. For any function to run, all of the functions it depends on should run before it can start. A function should start running as soon as all of its dependencies are satisfied.

Your program should take a target function name as input and read the dependency file to figure out dependencies of the target function and run the target function, only after running all its dependencies in the right order. It should also allow parallel execution of functions that don’t depend on each other, using some kind of multiprocessing with threads or processes.

For example a user could say run function_F. Then your code should run the in the following order:

Step 1    - run function A

Step 2.a - run function B - start as soon as dependent function A finishes

Step 2.b - run function C - start as soon as dependent function A finishes

Step 3.a - run function E - start as soon as dependent function B finishes

Step 3.b - run function D - start as soon as both dependent functions B and C finish 

Step 4    - run function F - start as soon as both dependent functions D and E finish

Steps 2.a and 2.b above should run in parallel, since both B and C depend on A and can start as soon as A finishes.

Step 3.a should start running function E as soon as function B in step 2.a finishes

Step 3.b should start running function D as soon as function B in step 2.a and function C in step 2.b finishes.

So steps 3.a and 3.b above may run in parallel, depending upon when function C in step 2.b finishes. 

Note that the function dependency graph described above are just an example. Your code should be able to work with any function dependencies described in a dependency graph in the format you choose. 

Expected deliverables —

1 - Some documentation describing the design of your code, interfaces, data structures used to represent the dependency graph etc.

2 - Working program that can run on any linux box, with clear requirements and a way to install any libraries/packages, if needed.

3 - A basic unit test that can be used to test your program with different input dependency graphs
