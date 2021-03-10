from calculator_framework import *
import math


# 1. Define your formulas
@register_formula([NumInput("radius")], decimal_places=3)
def volume_of_sphere(r):
    return 4 / 3 * math.pi * r ** 3


@register_formula([NumInput("radius")], decimal_places=3)
def surface_area_of_sphere(r):
    return 4 * math.pi * r ** 2


# 2. Start the command line prompt
run_calculator()
