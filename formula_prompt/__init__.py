"""
Library that allows registering formulas and then using them in your command prompt.

Important functions:

register_formula() -- Should be used as a function decorator to register
formulas into this library.

launch_prompt() -- Starts the prompt using the registered formulas.
"""
import functools
import math

from formula_prompt.inputs import *
from formula_prompt.navigation import NAVIGATION_ROOT, Formula

_DEFAULT_NUMBER_OF_DECIMALS = 4


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
        NAVIGATION_ROOT.add_formula(Formula(inner_function, func_inputs, name if name is not None else func.__name__))
        # Return the wrapped function
        return inner_function

    return decorator


def launch_prompt():
    """
    Launches the prompt at the navigation root folder.
    """
    NAVIGATION_ROOT.run()
