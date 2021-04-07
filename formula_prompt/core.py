#  Copyright (c) 2021 Martin Staadecker under the MIT License

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
    def __init__(self, func, inputs, name):
        super(Formula, self).__init__(name)
        self.func = func
        self.inputs = inputs

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
                print(f"{self.name}:\n{ans}")

            selection = input("\nEnter to run again or 0 to return...\n>>> ")
            if selection == "0":
                break