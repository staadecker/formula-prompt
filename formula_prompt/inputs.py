from formula_prompt.core import MAX_ENTRY_ATTEMPTS, UserInputError, DoneCollectingInput


class Input:
    """
    A parent class that can be extended to allow for different types of inputs to a formula.
    """
    # Internal list of preprocess to run before passing on the input
    # to the subclass. Allows for special handling of for example memory variables.
    _preprocesses = []
    # The way we actually get input from the user
    # Defined here so that it can be overwritten (e.g. to write tests)
    _reader = lambda: input(">>> ")

    @staticmethod
    def add_preprocess(preprocess):
        Input._preprocesses.append(preprocess)

    def __init__(self, name="data", optional=False):
        """Initialize the instance.

        Arguments:
            name: The name of the desired input, will be printed to the user before requesting
                the input.
            optional: Whether this input is required. This parameter should be handled by subclasses
                properly.
        """
        self.name = name
        self.optional = optional
        self.result = None

    def read(self):
        """Called by the program to retrieve the input value from the user."""
        # Print "Input <name>: " or "Input data: " if name isn't defined.
        print(f"Input {self.name}:")
        try:
            self.process(self.get_input)
        except DoneCollectingInput:
            pass
        return self.result

    def get_input(self):
        input = Input._reader()
        self.pre_process_input(input)
        return input

    def pre_process_input(self, input):
        if self.optional and input == "":
            raise DoneCollectingInput

        for preprocess in Input._preprocesses:
            preprocess_result = preprocess(input)
            if preprocess_result is None:
                continue

            self.result = preprocess_result
            raise DoneCollectingInput

    def process(self, get_input) -> None:
        """
        Function to be overridden by subclasses. Should read from input() and return
        the parsed value that will be passed on to the formula.
        """
        raise NotImplemented("Please use a subclass of Input such as NumInput or ListInput")


class NumInput(Input):
    """Input that accepts a number from the user."""

    def __init__(self, name="number", require_int=False, **kwargs):
        super(NumInput, self).__init__(name=name, **kwargs)
        self.require_int = require_int

    def process(self, get_input):
        for _ in range(MAX_ENTRY_ATTEMPTS):
            try:
                i = get_input()
                self.result = int(i) if self.require_int else float(i)
                return
            except ValueError:
                print("Invalid number. Try again.")
        raise UserInputError


class PercentInput(Input):
    """Input that accepts a percent value as either a decimal or a percent."""

    def __init__(self, name="number (percent)", **kwargs):
        super(PercentInput, self).__init__(name=name, **kwargs)

    def process(self, get_input):
        for _ in range(MAX_ENTRY_ATTEMPTS):
            try:
                str_i = get_input()
                float_i = float(str_i)
                if 0 <= float_i <= 1:
                    self.result = float_i
                elif 1 <= float_i <= 100:
                    self.result = float_i / 100
                else:
                    print("Invalid percent. Try again.")
                    continue
                return
            except ValueError:
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

    def process(self, get_input):
        self.result = []
        consecutive_failures = 0
        while True:
            try:
                i = get_input()
                self.result.append(float(i))
                consecutive_failures = 0
            except ValueError:
                if self.result and i == "":
                    break
                consecutive_failures += 1
                if consecutive_failures == MAX_ENTRY_ATTEMPTS:
                    raise UserInputError
                print("Invalid number. Try again.")


ALL_INPUT_TYPES = (ListInput, NumInput, IntInput, PercentInput)
