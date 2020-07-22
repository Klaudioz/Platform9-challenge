import json
import ast
import asyncio
from toposort import toposort, toposort_flatten

async def print_dependencies(list_of_dicts, target_function):
    for dict in list_of_dicts:
        if dict.__contains__(target_function):
            break
        else:
            # This part can be done asyncrously
            for elem in dict:
                await simple_function(elem)
                
async def simple_function(function_name):
    print("test: "+function_name)

try:
    with open("data.json", "r") as data:
        dictionary = ast.literal_eval(data.read())
        list_of_dicts = list(toposort(dictionary))
        print("List of Dependencies: ")
        print(list_of_dicts)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(print_dependencies(list_of_dicts, "F"))
        
except FileNotFoundError as err:
        print("File not found")
else:
    data.close()