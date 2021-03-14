import functools
import math

from formula_prompt.inputs import *
from formula_prompt.navigation import NAVIGATION_ROOT, Formula

"""
Library that allows registering formulas and then using them in your command prompt.

Important functions:

register_formula() -- Should be used as a function decorator to register
formulas into the library

formula_prompt() -- Starts the prompt using the registered formulas.
"""


_DEFAULT_NUMBER_OF_DECIMALS = 4

def register_formula(inputs, decimal_places=_DEFAULT_NUMBER_OF_DECIMALS, group=None):
    """
    Function decorator that adds a formula to the list of registered formulas

    :param inputs: Element of type <Input> or list of <Input> elements representing
    the inputs that should be passed to the formula
    :param decimal_places: Number of decimal places to round your answer to before printing
    """
    # If only one argument is passed, wrap it by a tuple
    if isinstance(inputs, Input):
        inputs = (inputs,)

    def decorator(func):
        @functools.wraps(func)
        def inner_function(*args, **kwargs):
            result = func(*args, **kwargs)
            if decimal_places is not None and isinstance(result, float) and not math.isnan(result):
                multiplier = 10 ** decimal_places
                result = round(result * multiplier) / multiplier

            return result

        NAVIGATION_ROOT.add_formula(Formula(inner_function, inputs), group)
        return inner_function

    return decorator


def launch_prompt():
    NAVIGATION_ROOT.run()
