from formula_prompt.shared import MAX_ENTRY_ATTEMPTS, UserInputError


class _Element:
    """Parent class of elements that can be listed. Subclass are Group and Formula"""

    def __init__(self, name):
        self.name = name

    def run(self):
        raise NotImplementedError

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        return self.name == other.name


class Formula(_Element):
    def __init__(self, func, inputs):
        super(Formula, self).__init__(func.__name__)
        self.func = func
        self.inputs = inputs

    def run(self):
        while True:
            inputs = []

            # For each required input, read the input and add it the list
            try:
                for input_description in self.inputs:
                    inputs.append(input_description.read())
            except UserInputError:
                break

            # Call the formula with the inputs
            ans = self.func(*inputs)

            # Print the results
            if ans is not None:
                print(f"{self.name}:\n{ans}")

            selection = input("\nEnter to run again or 1 to return...\n>>> ")
            if selection == "1":
                break


class _Group:
    """
    Equivalent to a folder or directory. Stores a set of subelements.
    """

    def __init__(self, name, is_root=False):
        self.name = name
        self.sub_elements = set()
        self.is_root = is_root

    def select_element(self):
        # Get all the sub elements (formulas and sub-groups) sorted by name
        elements = sorted(list(self.sub_elements), key=lambda x: x.name)

        if self.is_root:
            elements.append(_LeaveGroup("quit"))  # Add the option to quit the folder
        else:
            elements.insert(0, _LeaveGroup("go back"))

        # Print them out to the user
        for i, element in enumerate(elements):
            print(f"{i}:\t{element.name}")

        # Let the user pick
        for _ in range(MAX_ENTRY_ATTEMPTS):
            selection = input("Pick a formula:\n>>> ")

            try:
                return elements[int(selection)]
            except ValueError:
                print("Invalid input. Try again.")
            except IndexError:
                print("Invalid input. Try again.")
        raise UserInputError

    def run(self):
        while True:
            should_leave = self.select_element().run()

            if not self.is_root or should_leave:
                break

    def add_formula(self, formula, group):
        if group is None or group == "":
            self.sub_elements.add(formula)
        else:
            group, sep, subgroup = group.partition(".")

            for element in self.sub_elements:
                if isinstance(element, _Group) and element.name == group:
                    element.add_formula(formula, subgroup)
                    return

            new_group = _Group(group)
            new_group.add_formula(formula, subgroup)
            self.sub_elements.add(new_group)


class _LeaveGroup(_Element):
    def __init__(self, name):
        super(_LeaveGroup, self).__init__(name)

    def run(self):
        return True


NAVIGATION_ROOT = _Group(None, is_root=True)
