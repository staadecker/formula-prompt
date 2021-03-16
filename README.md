# Formula Prompt

This library let's you define formulas that you can later
evaluate in your command line. I use this library for school
work that requires repetitive calculations or calculations
needing a computer.

## Example

Here I define two formulas. Notice the `@register_formula(...)` decorator
that registers the formulas with the library.

```python
from formula_prompt import *

@register_formula([NumInput("side length")])
def volume_of_cube(s):
  return s ** 3

@register_formula([NumInput("length"), NumInput("width")])
def area_of_rectangle(length, width):
  return length * width
```
Now that the library has registered the formulas, I can launch the prompt.
```
launch_prompt()
```

The prompt lets you pick a formula and evaluate it.

```
0:	area_of_rectangle
1:	volume_of_cube
2:	quit
Pick a formula:
>>> 1
Input side length:
>>> 3
volume_of_cube:
27.0
```

For more examples, look at the [`/examples`](/examples) folder on GitHub.

## How to use this library

1. Install the library by running: `pip install formula-prompt`

2. Write your formulas (see example above).

3. Add the `@register_formula(...)` decorator (see below).

4. Call `launch_prompt()`.


### Using `@register_formula(...)`

`@register_formula(...)` is a decorator that takes in a few parameters.


name | Required | Description
--- | --- | ---
`func_inputs` | Yes | A list of objects describing the inputs to your formula (see allowed formula inputs section below).
`decimal_places` | No. Defaults to 4. | Decimal places to round the results of your formula to. Specify `None` to disable rounding.
`name` | No. Defaults to the function name. | Lets you set the name that will be displayed in the prompt. Names containing dots (`.`) will be considered folders. For example, `volumes.cube` will place the formula in a `volumes` folder and display the formula as `cube`.

### Allowed formula inputs

You can specify three types of inputs.

- `NumInput`: For inputs that accepts a single floating-point number.


- `IntInput`: For inputs that accept a single integer.


- `ListInput`: For inputs that accept a list of floating-point numbers.

You can use `optional=True` to allow skipping the input (this will pass `None`
to your function).

Here's an example.
```python
@register_formula([
    IntInput("first optional input", optional=True),
    NumInput("second non-optional input")
])
def some_funtion(first_integer_input, second_float_input):
    ...
```

You can also make a custom input type by creating a class that inherits from `Inputs`. See [`inputs.py`](/formula_prompt/inputs.py).