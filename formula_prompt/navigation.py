"""
navigation.py defines classes that allow the user to navigate between and pick formulas.
"""
from formula_prompt.core import *
from typing import List


class Folder(Element):
    """
    A folder or directory that can store other folders or formulas.
    """
    # Persistent content is content that is found across all folders
    _persistent_children: List[Element] = []

    @staticmethod
    def add_persistent_child(persistent_child: Element):
        """Add an element to all the folder"""
        Folder._persistent_children.append(persistent_child)

    def __init__(self, folder_name, is_root_folder=False):
        """
        :param folder_name: Folder name
        :param is_root_folder: Specifies if this is the root folder
        """
        super().__init__(folder_name)
        self.children = set()  # Contents of the folder, starts empty
        self.is_root_folder = is_root_folder
        self.leave_folder_child = _LeaveFolder(self.is_root_folder)

    def get_children(self) -> List[Element]:
        """Let the user pick a child of the folder and run it"""
        # Add the Leave Folder option and any persistent content
        children = [self.leave_folder_child] + Folder._persistent_children
        # Add the folders contents by name for easy navigation (base content always comes first)
        children.extend(sorted(list(self.children), key=lambda x: x.name))
        return children

    def select_child(self):
        children = self.get_children()

        # Print them contents of the folder to the user
        for i, element in enumerate(children):
            print(f"{i}:\t{element.name}")

        # Let the user pick a number representing the desired element
        for _ in range(MAX_ENTRY_ATTEMPTS):
            selection = input("Pick a formula:\n>>> ")

            try:
                return children[int(selection)]
            except ValueError:
                print("Invalid input. Try again.")
            except IndexError:
                print("Invalid input. Try again.")
        raise UserInputError

    def run(self):
        while True:
            # If there's only one element, select that element to run
            if len(self.children) == 1:
                element_to_run = next(iter(self.children))
            # Otherwise let the user pick
            else:
                element_to_run = self.select_child()

            # Run the element
            should_leave = element_to_run.run()

            # If we should leave break (which returns to parent folder)
            # Also if there was only one element break otherwise we have an
            # infinite loop
            if should_leave or len(self.children) <= 1:
                break


class _LeaveFolder(Element):
    """
    A simple element that will return True when run indicating the callee should exit its call loop.
    """

    def __init__(self, is_in_root):
        super().__init__("Quit" if is_in_root else "Go back")

    def run(self):
        return True
