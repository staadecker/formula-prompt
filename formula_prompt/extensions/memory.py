#  Copyright (c) 2021 Martin Staadecker under the MIT License
"""
Extension that adds the option to save an input
to a variable and then use it in other formulas
"""
from formula_prompt.inputs import ALL_INPUT_TYPES, Input
from formula_prompt.navigation import Folder
from formula_prompt.core import *
from typing import List

MEMORY = {}


class _AddToMemoryFolder(Folder):
    def __init__(self):
        super().__init__("Add to Memory")

        for input_type in ALL_INPUT_TYPES:
            self.children.add(_AddToMemory(input_type))

    def get_children(self) -> List[Element]:
        return [self.leave_folder_child] + list(self.children)


class _AddToMemory(Element):
    def __init__(self, input_type):
        self.input = input_type()
        super().__init__(input_type.__name__)

    def run(self):
        for _ in range(MAX_ENTRY_ATTEMPTS):
            print("Enter variable name")
            var_name = input(">>> ")
            if var_name == "" or not var_name.isalpha():
                print("Invalid input")
                continue

            MEMORY[var_name] = self.input.read()
            return True  # Return true to indicate we should leave parent folder


class _ReadFromMemory(Element):
    def __init__(self):
        super().__init__("Read from memory")

    def run(self):
        print(MEMORY)


def get_from_memory(key):
    return MEMORY.get(key, None)


def register_memory_plugin():
    Input.add_preprocess(get_from_memory)
    Folder.add_persistent_child(_AddToMemoryFolder())
    Folder.add_persistent_child(_ReadFromMemory())
