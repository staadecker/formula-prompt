# Calculator framework

This library let's you define formulas that you can then
evaluate in your command line. I use this library to do school
work where repetitive calculations are required.

## Example

For example, here's how you'd define formulas to find the
volume and surface area of a sphere.

```python
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

```

When you run this script here's what you get!

```
0:	surface_area_of_sphere
1:	volume_of_sphere
Pick a formula:
>>> 1
Input radius:
>>> 5
volume_of_sphere:
523.599

Enter to continue...
>>> 
```