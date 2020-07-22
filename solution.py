import json
import ast
import asyncio
from toposort import toposort, toposort_flatten

def main():
    """Takes a target function name as input and reading a dependency file run the target function, only after running all its dependencies in the right order.
    It gets the list of dependencies from a dictionary stored in a file and runs a simple function which print the name of the function.
    Because some functions don’t depend on each other, in that case can multithreading be used using asyncio.
    It uses Topological Sorting(toposort) to get the list of dependencies because these can't be represented with a tree, instead of that is needed a Directed Acyclic Graph (DAG).
    """
    # Variables
    filename = "data.json"
    target_function = "F"
    try:
        # Open file with list of dependencies written as a dictionary
        with open(filename, "r") as data:
            dictionary = ast.literal_eval(data.read())
            list_of_dicts = list(toposort(dictionary))
            print("List of Dependencies: " + str(list_of_dicts))
            # Create async loop
            loop = asyncio.get_event_loop()
            loop.run_until_complete(print_dependencies(list_of_dicts, target_function))
    except FileNotFoundError:
            print("File not found")
    else:
        data.close()

async def print_dependencies(list_of_dicts, target_function):
    """Run the target function, only after running all its dependencies in the right order
    Args:
        list_of_dicts (list): List of dictionaries with the dependencies list
        target_function (str): 
    Returns:
        Nothing. It's used to call the function run_function which it prints the results.
    Example:
        >>> list_of_dicts({"F": {"E", "D"}, "E": {"B"},"D": {"B","C"}, "C": {"A"}, "B": {"A"}},"F")
        List of Dependencies: [{'A'}, {'B', 'C'}, {'D', 'E'}, {'F'}]
        Run function: A
        Run function: B
        Run function: C
        Run function: D
        Run function: E
        Run function: F
    Explanation:
        Step 1 - run function A
        Step 2.a - run function B - start as soon as dependent function A finishes
        Step 2.b - run function C - start as soon as dependent function A finishes
        Step 3.a - run function E - start as soon as dependent function B finishes
        Step 3.b - run function D - start as soon as both dependent functions B and C finish
        Step 4 - run function F - start as soon as both dependent functions D and E finish
        Steps 2.a and 2.b above should run in parallel, since both B and C depend on A and can start as soon as A finishes.
        Step 3.a should start running function E as soon as function B in step 2.a finishes
        Step 3.b should start running function D as soon as function B in step 2.a and function C in step 2.b finishes.
        So steps 3.a and 3.b above may run in parallel, depending upon when function C in step 2.b finishes.

        Because steps 2.a and 2.b can run in parallel and the same for 3.a and 3.b there are in this case 4 correct answers:
        1.- Run function: A,B,C,D,E,F
        2.- Run function: A,B,C,E,D,F
        3.- Run function: A,C,B,D,E,F
        4.- Run function: A,C,B,E,D,F

    """
    for dict in list_of_dicts:
        for elem in dict:
            # This part can be done asynchronously
            await run_function(elem)
        if dict.__contains__(target_function):
            # No need to continue if it reaches the target_function
            break
            
async def run_function(target_function):
    """Prints the name of the target_function
    Args:
        target_function (str): Target function name
    Returns:
        Nothing. It prints the name of the function in the screen
    Example:
        >>> function_name="A"
        >>> run_function(a)
        Run function: A
    """
    print("Run function: " + target_function)

if __name__ == '__main__':
    main()