"""
navigation.py defines classes that allow the user to navigate between and pick formulas.
"""
from formula_prompt.shared import MAX_ENTRY_ATTEMPTS, UserInputError


class _Element:
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


class Formula(_Element):
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

            selection = input("\nEnter to run again or 1 to return...\n>>> ")
            if selection == "1":
                break


class _Folder:
    """
    A folder or directory that can store other folders or formulas.
    """

    def __init__(self, name, is_root=False):
        """
        :param name: Folder name
        :param is_root: Specifies if this is the root folder
        """
        self.name = name
        self.contents = set()  # Contents of the folder, starts empty
        self.is_root = is_root

    def pick_element(self):
        # Sorted the contents by name for easy navigation
        contents = sorted(list(self.contents), key=lambda x: x.name)

        if self.is_root:
            contents.append(_LeaveFolder("quit"))  # Add the option to quit the root folder (ends program)
        else:
            contents.insert(0, _LeaveFolder("go back"))  # Add option to go up one folder

        # Print them contents of the folder to the user
        for i, element in enumerate(contents):
            print(f"{i}:\t{element.name}")

        # Let the user pick a number representing the desired element
        for _ in range(MAX_ENTRY_ATTEMPTS):
            selection = input("Pick a formula:\n>>> ")

            try:
                return contents[int(selection)]
            except ValueError:
                print("Invalid input. Try again.")
            except IndexError:
                print("Invalid input. Try again.")
        raise UserInputError

    def run(self):
        while True:
            # Let the user pick an element and then run that element
            should_leave = self.pick_element().run()

            # If we should leave break (which returns to parent folder)
            if should_leave:
                break

    def add_formula(self, formula: Formula, path=None, depth=0):
        """
        Add a formula to the folder. Gets called recursiely if the formula lives in a nested folder.

        :param formula: The Formula to add
        :param path: A list of the names of all the folders and the formula
        :param depth: Current position in the list (how deep we are in the nested folders)
        """
        # If path isn't set, we create it by spliting the name at the dots ('.')
        if path is None:
            path = formula.name.split(".")

        # If we're at the end of the path (no more nested folders) we add the formula the current folder (self)
        if depth == len(path) - 1:
            self.contents.add(formula)
            return

        # Otherwise we need to go into the nested folder
        # The folders name is the formula name up the current folder
        folder_name = ".".join(path[:depth + 1])
        # We check if the folder already exists
        for element in self.contents:
            if isinstance(element, _Folder) and element.name == folder_name:
                # If it does, add the formula to that folder (recursive call)
                element.add_formula(formula, path, depth + 1)
                return

        # If the folder doesn't exist, we create it
        new_folder = _Folder(folder_name)
        # And add the formula to it (recursive call)
        new_folder.add_formula(formula, path, depth + 1)
        # And then add the folder to the current folder
        self.contents.add(new_folder)


class _LeaveFolder(_Element):
    """
    A simple element that will return True when run indicating the callee should exit its call loop.
    """

    def __init__(self, name):
        super(_LeaveFolder, self).__init__(name)

    def run(self):
        return True


# Initialize a root folder that one can add formulas to (via @register_formula decorator)
NAVIGATION_ROOT = _Folder(None, is_root=True)
