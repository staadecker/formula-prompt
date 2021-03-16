from formula_prompt import *

# 1. Define your formulas
@register_formula([NumInput("side length")])
def volume_of_cube(s):
    return s ** 3


@register_formula([NumInput("length"), NumInput("width")])
def area_of_rectangle(length, width):
    return length * width


# 2. Start the command line prompt
launch_prompt()
