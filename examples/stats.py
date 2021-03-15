"""
File containing a suite of statistics functions, some of which simply wrap statistical functions
from the 'scipy' library.

We use the 'formula_prompt' package to access and evaluate these functions in the terminal.
"""

from formula_prompt import *

import math
from scipy import stats
from scipy.special import gamma, gammainc


@register_formula(ListInput(), name="sample.mean")
def mean(x):
    return sum(x) / len(x)


@register_formula(ListInput(), name="sample.median")
def median(x):
    x = sorted(x)
    n = len(x)
    if n % 2 == 0:
        return (x[n // 2 - 1] + x[n // 2]) / 2
    else:
        return x[n // 2]


@register_formula(ListInput(), name="sample.variance")
def sample_variance(x):
    n = len(x)
    m = mean(x)
    s = 0
    for e in x:
        s += (e - m) ** 2
    return s / (n - 1)


@register_formula(ListInput(), name="sample.std")
def sample_std(x):
    return math.sqrt(sample_variance(x))


@register_formula(ListInput())
def sort(x):
    return sorted(x)


@register_formula([
    IntInput("x"),
    IntInput("n"),
    NumInput("p")
],
    name="distributions.binomial.binomial"
)
def binomial_distribution(x, n, p):
    return math.comb(n, x) * (p ** x) * ((1 - p) ** (n - x))


@register_formula([
    IntInput("x"),
    IntInput("n"),
    NumInput("p")
],
    name="distributions.binomial.cumulative"
)
def binomial_distribution_cumulative(x, n, p):
    return sum([binomial_distribution(i, n, p) for i in range(0, x + 1)])


@register_formula([
    IntInput("x"),
    IntInput("N"),
    IntInput("n"),
    IntInput("k")
], name="distributions.hyper geometric")
def hyper_geometric_dist(x, N, n, k):
    return math.comb(k, x) * math.comb(N - k, n - x) / math.comb(N, n)


@register_formula([
    IntInput("x"),
    IntInput("k"),
    NumInput("p")
], name="distributions.binomial.inverse")
def inv_binomial(x, k, p):
    return math.comb(x - 1, k - 1) * (p ** k) * ((1 - p) ** (x - k))


@register_formula([
    IntInput("x"),
    NumInput("mu"),
], name="distributions.poisson.poisson")
def poisson_dist(x, m):
    return math.exp(-m) * (m ** x) / math.factorial(x)


@register_formula([
    IntInput("x"),
    NumInput("mu"),
], name="distributions.poisson.cumulative")
def poisson_dist_cuml(x, m):
    return sum([poisson_dist(i, m) for i in range(0, x + 1)])


@register_formula([
    NumInput("z_lower", optional=True),
    NumInput("z_upper", optional=True)
], name="distributions.normal.cumulative")
def std_normal_dist_cuml(lower, upper):
    return evaluate_cumulative_distribution(stats.norm, lower, upper)


@register_formula([NumInput("alpha")], name="distributions.normal.inverse")
def cdf_to_z_values(a):
    return stats.norm.ppf(1 - a)


@register_formula([
    NumInput("lower incomplete", optional=True),
    NumInput("alpha")
])
def gamma_func(x, a):
    if x is None:
        return gamma(a)
    else:
        return gammainc(a, x) * gamma(a)


@register_formula([
    IntInput("v"),
    NumInput("alpha")
], name="distributions.chi2.inverse")
def inv_chi2_distribution(v, a):
    return stats.chi2.ppf(1 - a, v)


@register_formula([
    IntInput("v"),
    NumInput("lower_bound", optional=True),
    NumInput("upper_bound", optional=True)
], name="distributions.chi2.cumulative")
def chi2_cuml(v, lower, upper):
    return evaluate_cumulative_distribution(stats.chi2, lower, upper, v)


@register_formula([
    NumInput("v"),
    NumInput("alpha")
], name="distributions.t.inverse")
def inverse_t_dist(v, a):
    return stats.t.ppf(1 - a, v)


@register_formula([
    IntInput("v"),
    NumInput("lower_bound", optional=True),
    NumInput("upper_bound", optional=True)
], name="distributions.t.cumulative")
def t_dist_cuml(v, lower, upper):
    return evaluate_cumulative_distribution(stats.t, lower, upper, v)


@register_formula([
    IntInput("v1"),
    IntInput("v2"),
    NumInput("lower_bound", optional=True),
    NumInput("upper_bound", optional=True)
], name="distributions.f.cumulative")
def f_dist_cuml(v1, v2, lower, upper):
    return evaluate_cumulative_distribution(stats.f, lower, upper, v1, v2)


@register_formula([
    IntInput("v1"),
    IntInput("v2"),
    NumInput("alpha")
], name="distributions.f.inverse")
def f_dist_cuml(v1, v2, a):
    return stats.f.ppf(1 - a, v1, v2)


def evaluate_cumulative_distribution(distribution: stats.rv_continuous, lower, upper, *args):
    """
    Find the area between lower and upper in a scipy.stats continuous random variable
    """
    if lower is None and upper is None:
        print("Lower and upper bounds can't both be None")
        return
    if lower is None:
        return distribution.cdf(upper, *args)
    if upper is None:
        return 1 - distribution.cdf(lower, *args)
    return distribution.cdf(upper, *args) - distribution.cdf(lower, *args)


if __name__ == "__main__":
    launch_prompt()
