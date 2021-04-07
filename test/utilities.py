#  Copyright (c) 2021 Martin Staadecker under the MIT License
from formula_prompt.inputs import Input
from formula_prompt.core import Formula
from formula_prompt.setup import launch_prompt


def mock_reader(inputs):
    """Takes a list of inputs and that's what the reader will read"""
    iter_inputs = iter(inputs)

    def reader():
        return str(next(iter_inputs))

    Input.overwrite_reader(reader)


def run_and_capture(capture_func):
    Formula.override_print_result(capture_func)
    try:
        launch_prompt()
    except StopIteration:
        pass
