from formula_prompt import *


@register_formula([
    NumInput("Present value"),
    NumInput("Coupon value"),
    NumInput("Number of periods"),
    NumInput("Face value")
])
def find_yield(P, A, N, F):
    increment = 0.01
    y = 0.001
    threshold = 0.000005
    increasing = True

    def find_present(y):
        return A * (1 - (1 + y) ** (-N)) / y + F * (1 + y) ** (-N)

    while True:
        P_guess = find_present(y)

        if P - threshold < P_guess < P + threshold:
            break
        elif P_guess > P:
            y += increment
            if not increasing:
                increment /= 2
            increasing = True
        else:
            y -= increment
            if increasing:
                increment /= 2
            increasing = False
        # print(y)

    print(f"yield rate: %.3f +/- %.4f %%" % (y * 100, threshold * 100))


@register_formula([
    NumInput("number of periods"),
    PercentInput("rate")
])
def annuity_factor(N, r):
    factor = (1 - (1 + r) ** (-N)) / r
    return {"P/A": factor, "A/P": 1 / factor}

@register_formula([
    NumInput("number of periods"),
    PercentInput("rate"),
    PercentInput("gradient rate")
], name="factors.geometric gradient")
def geometric_factor(N, i, g):
    factor = (((1 + g) / (1 + i)) ** N - 1) / (g - i)
    return {"P/geom": factor, "geom/P": 1 / factor}


@register_formula([
    PercentInput("tax rate (t)"),
    PercentInput("CCA (depreciation) rate (d)"),
    PercentInput("interest rate (normally after-tax actual MARR/IRR) (i)")
], name="factors.CRF/CTF")
def tax_factors(t, d, i):
    return {"CRF": 1 - t * d / (i + d), "CTF": 1 - t * d / (i + d) * (1 + i / 2) / (1 + i)}


@register_formula([
    NumInput("number of periods (n)"),
    PercentInput("rate (percent)")
], name="factors.annual")
def annual_factor(N, i):
    factor = (1 - (1+i) ** (-N)) / i
    return {"P/A": factor, "A/P": 1 / factor}

@register_formula([
    NumInput("n"),
    PercentInput("rate")
], name="factors.future")
def future_factor(N, i):
    factor = (1+i) ** N
    return { "P/F": 1 / factor , "F/P": factor }

@register_formula([
    NumInput("n"),
    PercentInput("rate")
], name="factors.arithmetic_grad")
def arithmetic_gradient_factor(N, i):
    factor = (1 - (1 + i * N) / (1 + i) ** N) / (i ** 2)
    return { "P/G": factor, "G/P": 1 / factor }


if __name__ == "__main__":
    launch_prompt()
