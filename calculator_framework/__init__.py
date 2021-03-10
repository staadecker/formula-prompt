import functools

"""
Library that allows registering formulas and then using them in a calculator.

Important functions:

register_formula() -- Should be used as a function decorator to register
formulas into the library

run_calculator() -- Starts the calculator using the registered formulas.
"""

_REGISTERED_FORMULAS = []

_MAX_ENTRY_ATTEMPTS = 3


class UserInputError(Exception):
    """Custom error type raised when the user repeatedly enters invalid values."""
    pass


class Input:
    """
    A parent class that can be extended to allow for different types of inputs to a formula.

    Important functions:

    read() -- Called by the Calculator instance to retrieve the input value from the user.

    process() -- Function to be overridden by subclasses. Should read from input() and return
            the parsed value that will be passed on to the formula.
    """

    def __init__(self, name, optional=False):
        """Initialize the instance.

        Arguments:
            name: The name of the desired input, will be printed to the user before requesting
                the input.
            optional: Whether this input is required. This parameter should be handled by subclasses
                properly.
        """
        self.name = name
        self.optional = optional

    def read(self):
        # Print "Input <name>: " or "Input data: " if name isn't defined.
        print("Input {}:".format(self.name if self.name is not None else "data"))
        return self.process()

    def process(self):
        raise NotImplemented("Please use a subclass of Input such as NumInput or ListInput")


class NumInput(Input):
    """Input that accepts a number from the user."""

    def __init__(self, name="number", require_int=False, **kwargs):
        super(NumInput, self).__init__(name=name, **kwargs)
        self.require_int = require_int

    def process(self):
        for _ in range(_MAX_ENTRY_ATTEMPTS):
            try:
                i = input(">>> ")
                if self.require_int:
                    return int(i)
                else:
                    return float(i)
            except ValueError as e:
                if self.optional and i == "":
                    return None
                print("Invalid number")
        raise UserInputError


class IntInput(NumInput):
    """Input that accepts an integer from the user."""

    def __init__(self, name="integer", **kwargs):
        super(IntInput, self).__init__(name, require_int=True, **kwargs)


class ListInput(Input):
    """Input that accepts a list of numbers from the user."""

    def __init__(self, name="list", **kwargs):
        super(ListInput, self).__init__(name=name, **kwargs)

    def process(self):
        values = []
        consecutive_failures = 0
        while True:
            try:
                i = input(">>> ")
                values.append(float(i))
                consecutive_failures = 0
            except ValueError:
                if (values or self.optional) and i == "":
                    return values
                consecutive_failures += 1
                if consecutive_failures == _MAX_ENTRY_ATTEMPTS:
                    raise UserInputError
                print("Invalid number")


def register_formula(inputs, decimal_places=None):
    """
    Function decorator that adds a formula to the list of registered formulas

    :param inputs: Element of type <Input> or list of <Input> elements representing
    the inputs that should be passed to the formula
    """
    # If only one argument is passed, wrap it by a tuple
    if isinstance(inputs, Input):
        inputs = (inputs,)

    def decorator(func):
        @functools.wraps(func)
        def inner_function(*args, **kwargs):
            result = func(*args, **kwargs)
            if decimal_places is not None and type(result) == float:
                multiplier = 10 ** decimal_places
                result = round(result * multiplier) / multiplier

            return result

        inner_function.inputs = inputs
        _REGISTERED_FORMULAS.append(inner_function)
        return inner_function

    return decorator


def run_calculator():
    """
    Infinite loop that
    1. Reads from the command line the formula the user wants to call
    2. Reads from the command line the inputs for that formula
    3. Executes that formula
    4. Prints the result.
    """
    global _REGISTERED_FORMULAS

    # Order the registered formulas by name
    _REGISTERED_FORMULAS = sorted(_REGISTERED_FORMULAS, key=lambda f: f.__name__)

    formula = None
    while True:
        # Let the user pick the formula they wish to use
        formula = pick_formula(formula)

        inputs = []

        # For each required input, read the input and add it the list
        for input_description in formula.inputs:
            inputs.append(input_description.read())

        # Call the formula with the inputs
        ans = formula(*inputs)

        # Print the results
        if ans is not None:
            print(f"{formula.__name__}:\n{ans}")

        input("\nEnter to continue...\n>>> ")


def pick_formula(prev_formula):
    """Let's a user select a formula from the registered formulas"""
    for i, formula in enumerate(_REGISTERED_FORMULAS):
        print(f"{i}:\t{formula.__name__}")
    for _ in range(_MAX_ENTRY_ATTEMPTS):
        selection = input("Pick a formula:\n>>> ")

        try:
            return _REGISTERED_FORMULAS[int(selection)]
        except ValueError:
            if selection == "" and prev_formula is not None:
                return prev_formula
            print("Invalid input")
    raise UserInputError
