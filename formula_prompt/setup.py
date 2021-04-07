#  Copyright (c) 2021 Martin Staadecker under the MIT License

"""
Library that allows registering formulas and then using them in your command prompt.

Important functions:

register_formula() -- Should be used as a function decorator to register
formulas into this library.

launch_prompt() -- Starts the prompt using the registered formulas.
"""
import functools
import math

from formula_prompt.core import *
from formula_prompt.inputs import Input
from formula_prompt.navigation import Folder
from formula_prompt.extensions.memory import register_memory_extension

_DEFAULT_NUMBER_OF_DECIMALS = 4

# Initialize a root folder that one can add formulas to (via @register_formula decorator)
NAVIGATION_ROOT = Folder(None, is_root_folder=True)


def register_formula(func_inputs, decimal_places=_DEFAULT_NUMBER_OF_DECIMALS, name=None):
    """
    Function decorator that adds a formula to the list of registered formulas

    :param func_inputs: Element of type <Input> or list of <Input> elements representing
    the inputs that should be passed to the formula
    :param decimal_places: Number of decimal places to round your answer to before printing
    :param name: A name for the function. If the name contains '.', this will be considered as a folder.
    """
    # If only one argument is passed, wrap it by a tuple
    if isinstance(func_inputs, Input):
        func_inputs = (func_inputs,)

    # Define the decorator
    def decorator(func):
        @functools.wraps(func)  # Make func.__name__ keeps its value
        # Define function to be called when func is called
        def inner_function(*args, **kwargs):
            result = func(*args, **kwargs)  # Call the function

            if decimal_places is not None:
                # Round the result if the result is a float
                if isinstance(result, float) and not math.isnan(result):
                    result = round(result, ndigits=decimal_places)

                # Round the result if the result is a dict
                elif isinstance(result, dict):
                    for key, val in result.items():
                        if isinstance(val, float) and not math.isnan(val):
                            result[key] = round(val, decimal_places)

            return result

        # Register the formula in the root folder (the folder will handle placing it in the right location)
        _add_formula(NAVIGATION_ROOT.children,
                     Formula(inner_function, func_inputs, name if name is not None else func.__name__))
        # Return the wrapped function
        return inner_function

    return decorator


def _add_formula(contents, formula: Formula, path=None, depth=0):
    """
    Add a formula to the folder. Gets called recursively if the formula lives in a nested folder.

    :param formula: The Formula to add
    :param path: A list of the names of all the folders and the formula
    :param depth: Current position in the list (how deep we are in the nested folders)
    """
    # If path isn't set, we create it by splitting the name at the dots ('.')
    if path is None:
        path = formula.name.split(".")

    # If we're at the end of the path (no more nested folders) we add the formula the current folder (self)
    if depth == len(path):
        contents.add(formula)
        return

    # Otherwise we need to go into the nested folder
    # The folders name is the formula name up the current folder
    folder_name = ".".join(path[:depth + 1])
    # We check if the folder already exists
    for element in contents:
        if isinstance(element, Folder) and element.name == folder_name:
            # If it does, add the formula to that folder (recursive call)
            _add_formula(element.children, formula, path, depth + 1)
            return

    # If the folder doesn't exist, we create it
    new_folder = Folder(folder_name)
    # And add the formula to it (recursive call)
    _add_formula(new_folder.children, formula, path, depth + 1)
    # And then add the folder to the current folder
    contents.add(new_folder)


def launch_prompt(enable_memory=True):
    """
    Launches the prompt at the navigation root folder.
    """
    if enable_memory:
        register_memory_extension()
    NAVIGATION_ROOT.run()
