# Calculator framework

This library let's you define formulas that you can later
evaluate in your command line. I use this library for school
work that requires doing repetitive calculations or calculations
needing a computer.

## Example

Here's how you'd define formulas to find the
volume of a cube and rectangular prism.

```python
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
```

When you run this file, a prompt will let you evaluate your
formulas. Here's what it looks like!

```
0:	volume_of_cube
1:	volume_of_rectangular_prism
Pick a formula:
>>> 0
Input side length:
>>> 2
volume_of_cube:
8.0

Press enter to run again...
>>> 
```

For more examples, look at the `examples` folder on GitHub.

## Usage details

### Installation

Simply run: `pip install calculator-framework`

### Setting up your code

To use this library:

1. Define your functions for each of your formulas.
   Don't worry about reading user input, this is handled by the library!
   

2. Add the `@register_formula(...)` decorator to your function. This will
register you function will the library.

   
3. Run `launch_calculator()` to start the prompt.

### Using `@register_formula(...)`

This is where the good stuff happens!

`@register_formula(...)` is a decorator that takes in a list
of objects that describe the inputs to your formula.

These objects can be instance of the following classes:

- `NumInput`: For inputs that accepts a single floating-point number.


- `IntInput`: For inputs that accept a single integer.


- `ListInput`: For inputs that accept a list of floating-point numbers.

You can use `optional=True` to allow skipping the input (this will pass `None`
to your function).

Here's an example.
```
@register_formula([
    IntInput("first optional input", optional=True),
    NumInput("second non-optional input")
])
def some_funtion(...):
    ...
```

### Advanced details

- If `ListInput`, `IntInput` or `NumInput` don't meet your needs, you can
define a custom class that inherits from `Input` and implements `process()`.
  Look at how `NumInput` is implemented for an example.


- You can specify the number of decimals to round the result to by 
  either a) overwriting the
global variable `DEFAULT_NUMBER_OF_DECIMALS` or by b) passing`decimal_places=`
  as an argument to the `@register_function(...)` decorator. To not round
  the result, set the argument to `None`.
  

- If your function only has one input, you don't need to pass in a list.
For example, `@register_formula(NumInput("x"))` works the same as
  `@register_formula([NumInput("x")])`