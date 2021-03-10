REGISTERED_FORMULAS = []


class Input:
    def __init__(self, name=None, optional=False):
        self.name = name
        self.optional = optional

    def read(self):
        print("Input {}:".format(self.name if self.name is not None else "data"))
        return self.process()

    def process(self):
        raise NotImplemented("Please use a subclass of Input such as NumInput or ListInput")


class NumInput(Input):
    def __init__(self, name=None, require_int=False, **kwargs):
        if name is None:
            name = "integer" if require_int else "number"

        super(NumInput, self).__init__(name=name, **kwargs)
        self.require_int = require_int

    def process(self):
        while True:
            try:
                i = input()
                if self.require_int:
                    return int(i)
                else:
                    return float(i)
            except ValueError as e:
                if self.optional and i == "":
                    return None
                print("Invalid input")


class ListInput(Input):
    def __init__(self, name="list", **kwargs):
        super(ListInput, self).__init__(name=name, **kwargs)

    def process(self):
        values = []
        while True:
            try:
                i = input()
                values.append(float(i))
            except ValueError:
                if (values or self.optional) and i == "":
                    return values
                print("Invalid input")


def register(inputs):
    # If only one argument pass wrap it by a tuple
    if type(inputs) == Input:
        inputs = (inputs,)

    def decorator(func):
        func.inputs = inputs
        REGISTERED_FORMULAS.append(func)
        return func

    return decorator


class Calculator:
    @staticmethod
    def launch():
        """
        Infinite loop that
        1. Reads from the command line the formula I want to call
        2. Reads from the command line the arrays (data) I want to use
        3. Executes that formula
        4. Prints the result.
        """
        global REGISTERED_FORMULAS
        REGISTERED_FORMULAS = sorted(REGISTERED_FORMULAS, key=lambda f: f.__name__)

        formula = None
        while True:
            formula = Calculator.get_formula(formula)

            inputs = []

            for input_description in formula.inputs:
                inputs.append(input_description.read())

            ans = formula(*inputs)
            if ans is not None:
                print(f"{formula.__name__}: ")
                print(ans)
            print()
            input()

    @staticmethod
    def get_formula(prev_formula):
        """
        Finds the formula I want to call within Util, based on the command line
        input.
        """
        print("Formulas: ")
        for i, formula in enumerate(REGISTERED_FORMULAS):
            print("{}:\t{}".format(i, formula.__name__))
        while True:
            selection = input("Formula to evaluate: ")

            try:
                return REGISTERED_FORMULAS[int(selection)]
            except ValueError:
                if selection == "" and prev_formula is not None:
                    return prev_formula
                print("Invalid input")
