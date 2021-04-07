#  Copyright (c) 2021 Martin Staadecker under the MIT License

import math

# Max number of wrong entries before aborting operation
MAX_ENTRY_ATTEMPTS = 3


class UserInputError(Exception):
    """Custom error type raised when the user repeatedly enters invalid values."""
    pass


class DoneCollectingInput(Exception):
    """
    Custom error type raised to indicate that
    we are done collecting the user's input.
    """
    pass


class Element:
    """Element that can be displayed in the Navigation. Sub-classes include Folder and Formula"""

    def __init__(self, name):
        """
        :param name: Name to display in the navigation
        """
        self.name = name

    def run(self):
        """
        Called when the element is selected during navigation
        """
        raise NotImplementedError


class Formula(Element):
    _print_result = print

    @staticmethod
    def override_print_result(printer):
        Formula._print_result = printer

    def __init__(self, func, inputs, name, decimal_places=None):
        super(Formula, self).__init__(name)
        self.func = func
        self.inputs = inputs
        self.decimal_places = decimal_places

    def run(self):
        while True:
            inputs = []

            # For each required input, read the input and add it the list
            try:
                for input_description in self.inputs:
                    inputs.append(input_description.read())
            # If the user fails to enter an input, cancel the formula
            except UserInputError:
                break

            # Call the formula with the inputs
            ans = self.func(*inputs)

            # Print the results
            if ans is not None:
                if self.decimal_places is not None:
                    ans = self.round_result(ans)

                print(f"{self.name}:")
                Formula._print_result(ans)

            selection = input("\nEnter to run again or 0 to return...\n>>> ")
            if selection == "0":
                break

    def round_result(self, result):
        # Round the result if the result is a float
        if isinstance(result, float) and not math.isnan(result):
            result = round(result, ndigits=self.decimal_places)

        # Round the result if the result is a dict
        elif isinstance(result, dict):
            for key, val in result.items():
                if isinstance(val, float) and not math.isnan(val):
                    result[key] = round(val, self.decimal_places)

        return result