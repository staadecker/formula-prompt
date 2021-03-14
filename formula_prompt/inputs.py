from formula_prompt.shared import MAX_ENTRY_ATTEMPTS, UserInputError


class Input:
    """
    A parent class that can be extended to allow for different types of inputs to a formula.

    Important functions:

    read() -- Called by the program to retrieve the input value from the user.

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
        for _ in range(MAX_ENTRY_ATTEMPTS):
            try:
                i = input(">>> ")
                if self.require_int:
                    return int(i)
                else:
                    return float(i)
            except ValueError as e:
                if self.optional and i == "":
                    return None
                print("Invalid number. Try again.")
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
                if consecutive_failures == MAX_ENTRY_ATTEMPTS:
                    raise UserInputError
                print("Invalid number. Try again.")