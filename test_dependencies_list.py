import ast
import asyncio
import unittest
import os
from toposort import toposort, toposort_flatten
from dependencies_list import print_dependencies

class TestDependenciesList(unittest.TestCase):
    """Test class which takes a target function name as input and reading a dependency file run the target function, only after running all its dependencies in the right order.
    It gets the list of dependencies from a list of elements stored in a file (the first element is a dictionary) and runs a simple function which print the name of the function.
    It uses the rest of the elements of the list (which all are lists) as a possible expected results. Because some steps can run in parallel there are multiple possible results.
    Just one of the possible results need to match with the results of the function to pass the test.
    """
    filesize=0
    def test_dependencies_list(self):
        filename = "test_data.json"
        target_function = "F"
        try:
            # Open file with list of dependencies written as a dictionary and multiple correct solutions
            with open(filename, "r") as data:
                list_of_results = []
                dictionary = ast.literal_eval(data.read())
                # Using a global variable
                TestDependenciesList.filesize = len(dictionary)
                # Getting just the first element with the list of dependencies
                list_of_dicts = list(toposort(dictionary[0]))
                # Create async loop
                loop = asyncio.get_event_loop()
                list_of_results = loop.run_until_complete(print_dependencies(list_of_dicts, target_function))
                # Ignoring first element of the file (Not part of the possible solutions)
                for dict in dictionary[1:]:
                    # Without a subtest, execution would stop after the first failure
                    with self.subTest(dict=dict):
                        self.assertEqual(list_of_results, dict)
                return (dictionary[1:])
        except FileNotFoundError:
                print("File not found")
        else:
            data.close()

if __name__ == '__main__':
    alltests = unittest.TestLoader().loadTestsFromTestCase(TestDependenciesList)
    # Making the TextTestRunner quiet pointing it to a null stream
    runner = unittest.TextTestRunner(stream=open(os.devnull, 'w'))
    result = runner.run(alltests)
    # Comparing number of failures and errors with size of the list of possible results
    if len(result.failures) + len(result.errors) == TestDependenciesList.filesize-1:
        print('Test FAILED')
    else:
        print('Test OK')
    """It's very tricky but it can be validated very easily just replacing in the file with the results all the instances of: "Run function: A" with "Run function: 1"
    # I'd to use that because I was unable to find a way to have the test approved when only one possible case is ok. It's because of multithreading, always there are multiple
    # possible cases and only one is correct
    """