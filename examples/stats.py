from calculator_framework import *

import math
from scipy.stats import norm
from scipy.special import gamma, gammainc

"""
Stats class contains all the functions that this program offers. Namely,

mean, median, sample_variance, sample_std (sample standard deviation) and sort.

These methods are very straight forward, they take in a list and return the result.
"""


@register_formula(ListInput())
def mean(x):
    return sum(x) / len(x)


@register_formula(ListInput())
def median(x):
    x = sorted(x)
    n = len(x)
    if n % 2 == 0:
        return (x[n // 2 - 1] + x[n // 2]) / 2
    else:
        return x[n // 2]


@register_formula(ListInput())
def sample_variance(x):
    n = len(x)
    m = mean(x)
    s = 0
    for e in x:
        s += (e - m) ** 2
    return s / (n - 1)


@register_formula(ListInput())
def sample_std(x):
    return math.sqrt(sample_variance(x))


@register_formula(ListInput())
def sort(x):
    return sorted(x)


@register_formula([
    IntInput("x"),
    IntInput("n"),
    NumInput("p")
])
def binomial_dist(x, n, p):
    return math.comb(n, x) * (p ** x) * ((1 - p) ** (n - x))


@register_formula([
    IntInput("x"),
    IntInput("n"),
    NumInput("p")
])
def binomial_dist_cuml(x, n, p):
    return sum([binomial_dist(i, n, p) for i in range(0, x + 1)])


def _description_hypergeo_dist():
    return ("x", int), ("N", int), ("n", int), ("k", int)


@register_formula([
    IntInput("x"),
    IntInput("N"),
    IntInput("n"),
    IntInput("k")
])
def hypergeo_dist(x, N, n, k):
    return math.comb(k, x) * math.comb(N - k, n - x) / math.comb(N, n)


@register_formula([
    IntInput("x"),
    IntInput("k"),
    NumInput("p")
])
def inv_binomial(x, k, p):
    return math.comb(x - 1, k - 1) * (p ** k) * ((1 - p) ** (x - k))


@register_formula([
    IntInput("x"),
    NumInput("mu"),
])
def poisson_dist(x, m):
    return math.exp(-m) * (m ** x) / math.factorial(x)


@register_formula([
    IntInput("x"),
    NumInput("mu"),
])
def poisson_dist_cuml(x, m):
    return sum([poisson_dist(i, m) for i in range(0, x + 1)])


@register_formula([
    NumInput("z_lower", optional=True),
    NumInput("z_upper", optional=True)
])
def std_normal_dist_cuml(z_low, z_end):
    if z_low is None and z_end is None:
        print("Lower and upper bounds can't both be None")
        return
    if z_low is None:
        return norm.cdf(z_end)
    if z_end is None:
        return 1 - norm.cdf(z_low)
    return norm.cdf(z_end) - norm.cdf(z_low)


@register_formula([NumInput("percent below z")])
def cdf_to_z_values(cdf):
    return norm.ppf(cdf)


@register_formula([
    NumInput("lower incomplete", optional=True),
    NumInput("alpha")
])
def gamma_func(x, a):
    if x is None:
        return gamma(a)
    else:
        return gammainc(a, x) * gamma(a)


if __name__ == "__main__":
    launch_calculator()
