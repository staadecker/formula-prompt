from calculator_framework import *


# 1. Define your formulas
@register_formula([NumInput("side length")])
def volume_of_cube(s):
    return s ** 3


@register_formula([
    NumInput("length"),
    NumInput("width"),
    NumInput("height")
])
def volume_of_rectangular_prism(length, width, height):
    return length * width * height


# 2. Start the command line prompt
launch_calculator()
