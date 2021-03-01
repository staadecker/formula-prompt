class FormulaSet:
    def __init__(self, formula_class, except_many_functions=False):
        self.formulas, self.formula_descriptions = self.parse_formula_class(formula_class)
        self.expect_many_functions = except_many_functions

    @staticmethod
    def parse_formula_class(formula_class):
        formulas = {f: getattr(formula_class, f) for f in dir(formula_class) if f[0] != "_"}
        formula_descriptions = {}

        for name in formulas.keys():
            try:
                formula_descriptions[name] = getattr(formula_class, "_description_" + name)()
            except:
                formula_descriptions[name] = None

        print(formulas, formula_descriptions)

        return formulas, formula_descriptions

    def run(self):
        """
        Infinite loop that
        1. Reads from the command line the function I want to call
        2. Reads from the command line the arrays (data) I want to use
        3. Executes that function
        4. Prints the result.
        """
        formulas = []
        while True:
            formulas = self.get_functions(formulas)

            if self.formula_descriptions[formulas[0]] is None:
                f_in = self.read_many_arrays()
            else:
                f_in = self.read_input(self.formula_descriptions[formulas[0]])

            for name in formulas:
                ans = self.formulas[name](*f_in)
                if ans is not None:
                    print(f"{self.formulas[name].__name__}: ")
                    print(ans)
                print()


    def read_input_arr(self, name=None, numerical=True):
        """
        Reads an array of values from the shell / command line.
        """
        if name is None:
            if numerical:
                print("Input numerical data:")
            else:
                print("Input data:")
        else:
            print(f"Input {name}")

        data = []
        while True:
            i = input()
            if i == "":
                break
            if numerical:
                i = float(i)
            data.append(i)
        return data

    def read_many_arrays(self):
        """
        Will use read_input_arr() multiple times, to read many input arrays.

        Currently all our Util functions take just one array as input, however if
        a future function takes 2 arrays, this would allow me to input both.
        """
        arrays = []

        while True:
            array = self.read_input_arr()
            if array == []:
                break
            arrays.append(array)

        return arrays

    def get_functions(self, prev_functions):
        """
        Finds the function I want to call within Util, based on the command line
        input.
        """
        formula_map = {}
        for i, function in enumerate(self.formulas.keys()):
            formula_map[i] = function
        print("Functions:", formula_map)
        functions = []
        while True:
            f = input("Function to evaluate:")
            if f == "":
                break
            try:
                functions.append(formula_map[int(f)])
                if not self.expect_many_functions:
                    break
            except:
                print("Invalid function")

        return functions if functions else prev_functions

    def read_input(self, input_descriptions):
        if type(input_descriptions) == tuple:
            return self.read_old_input(input_descriptions)

        input_arr = []

        for input_description in input_descriptions["inputs"]:

            while True:
                try:
                    value_str = input("%s : " % input_description["name"])

                    if "optional" in input_description and input_description["optional"]:
                        if value_str == "":
                            input_arr.append(None)
                            break

                    value = input_description["parse"](value_str)
                    input_arr.append(value)
                    break
                except BaseException as e:
                    print("Invalid input.")
                    print(e)

        return input_arr





    def read_old_input(self, input_description):
        input_arr = []
        for input_name, input_type in input_description:
            while True:
                try:
                    value_str = input("%s : " % input_name)

                    value = input_type(value_str)
                    input_arr.append(value)
                    break
                except:
                    print("Invalid input.")
        return input_arr
