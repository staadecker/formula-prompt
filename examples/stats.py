"""
File containing a suite of statistics functions, some of which simply wrap the scipy library.

I use the 'formula_prompt' package to access and evaluate these functions in the terminal.
The @register_formula decorator is used to register my formulas with the package.
More information about this package can be found at https://pypi.org/project/formula-prompt/.

Note that the formula names are indicated in @register_formula(..., name=<>).
"""

from formula_prompt import *

import math
from scipy import stats
from scipy.special import gamma, gammainc


@register_formula(ListInput(), name="sample.mean")
def mean(x):
    """Find the mean of a sample by summing the values and dividing by the size of the sample."""
    return sum(x) / len(x)


@register_formula(ListInput(), name="sample.median")
def median(x):
    """Find the median of a sample by sorting the sample and then returning the middle element."""
    x = sorted(x)  # Sort the sample
    n = len(x)
    middle = n // 2
    if n % 2 == 0:
        # If there's an even number of elements, the median is an average of the two middle values
        return 0.5 * (x[middle - 1] + x[middle])
    else:
        # If there's an odd number of elements, the median is the middle element
        return x[middle]


@register_formula(ListInput(), name="sample.variance")
def sample_variance(x):
    """Find the variance of a sample by summing (x-mean)^2 over each element x, then dividing by (n-1)"""
    n = len(x)
    m = mean(x)
    s = 0  # s is our sum
    for xi in x:  # For every element xi in sample x
        s += (xi - m) ** 2  # Add (xi - m)**2 to our sum s
    return s / (n - 1)  # Then divide the sum by n-1


@register_formula(ListInput(), name="sample.std")
def sample_std(x):
    """Find the sample standard deviation by taking the square root of the sample variance."""
    return math.sqrt(sample_variance(x))


@register_formula(ListInput(), name="sort")
def sort(x):
    """Return the sample x in increasing order."""
    return sorted(x)


@register_formula([
    IntInput("x"),
    IntInput("n"),
    NumInput("p")
],
    name="distributions.binomial"
)
def binomial_distribution(x, n, p):
    """
    Evaluate the binomial distribution b(x; n, p) as defined in the textbook.

    Equivalent to finding the probability of getting x heads when flipping
    a coin n times and the likeliness of getting heads on any one flip is p.

    The equation used is nCx * p ^ x * (1-p) ^ (n-x).
    """
    return math.comb(n, x) * (p ** x) * ((1 - p) ** (n - x))


@register_formula([
    IntInput("x"),
    IntInput("n"),
    NumInput("p")
],
    name="distributions.binomial.cumulative"
)
def binomial_distribution_cumulative(x, n, p):
    """
    Evaluate the cumulative binomial distribution B(x; n, p).

    Equivalent to finding the probability of getting between 0 and x heads
    when flipping a coin n times and the likeliness of getting heads on any one flip is p.

    Found by summing the binomial distribution from 0 up to x.
    """
    return sum([binomial_distribution(i, n, p) for i in range(0, x + 1)])


@register_formula([
    IntInput("x"),
    IntInput("N"),
    IntInput("n"),
    IntInput("k")
], name="distributions.hypergeometric")
def hypergeometric_dist(x, N, n, k):
    """
    Evaluate the hypergeometric distribution h(x; N, n, k) as defined in the textbook.

    Equivalent to the probability of getting x blue socks when picking n socks from a total
    of N socks where a total of k socks are blue.

    Found with the equation kCx * (N-k)C(n-x) / NCn
    """
    return math.comb(k, x) * math.comb(N - k, n - x) / math.comb(N, n)


@register_formula([
    IntInput("x"),
    IntInput("k"),
    NumInput("p")
], name="distributions.negative_binomial")
def negative_binomial(x, k, p):
    """
    Evaluate the negative binomial distribution b*(x; k, p) as defined in the textbook.

    Equivalent to finding the probability of coin flip x to be the k-th head when the
    probability of getting a head on any one coin flip is p.

    Found with the equation (x-1)C(k-1) * p^k * (1 - p)^(x - k)
    """
    return math.comb(x - 1, k - 1) * (p ** k) * ((1 - p) ** (x - k))


@register_formula([
    IntInput("x"),
    IntInput("k"),
    NumInput("p")
], name="distributions.negative_binomial.cumulative")
def negative_binomial_cumulative(x, k, p):
    """
    Evaluate the cumulative negative binomial distribution by summing
    the negative binomial distribution from k to x (inclusive).
    """
    return sum([negative_binomial(xi, k, p) for xi in range(k, x + 1)])


@register_formula([
    IntInput("x"),
    NumInput("mu"),
], name="distributions.poisson")
def poisson_dist(x, m):
    """
    Evaluate the poisson distribution p(x; m) where x is the number
    of outcomes that occur in a given interval and m is the mean
    of the distribution (which equals the rate of occurrence times
    the size of the interval).
    """
    return math.exp(-m) * (m ** x) / math.factorial(x)


@register_formula([
    IntInput("x"),
    NumInput("mu"),
], name="distributions.poisson.cumulative")
def poisson_dist_cumulative(x, m):
    """
    Evaluate the cumulative poisson distribution P(x; m) by summing the
    poisson distribution (defined above) from 0 up to x (inclusive).
    """
    return sum([poisson_dist(i, m) for i in range(0, x + 1)])


@register_formula([
    NumInput("lower bound", optional=True),
    NumInput("upper bound", optional=True)
], name="distributions.normal.cumulative")
def std_normal_dist_cumulative(lower, upper):
    """
    Find the area under the standard normal distribution between
    the lower and upper bounds.

    Bounds that aren't specified are taken at infinity.
    """
    return find_distribution_area(stats.norm, lower, upper)


@register_formula([NumInput("alpha")], name="distributions.normal.inverse")
def normal_dist_inverse(a):
    """
    Given an area 'a', return the z-value that if taken as a lower bound
    results in the standard normal distribution having 'a' area above it.
    """
    return stats.norm.ppf(1 - a)


@register_formula([
    NumInput("alpha"),
    NumInput("upper bound", optional=True)
], name="gamma_function")
def gamma_func(a, x):
    """
    Evaluate the incomplete gamma function with parameter alpha (a) up to x.
    If x is not specified, evaluate the complete gamma function (up to infinity).
    """
    if x is None:
        return gamma(a)
    else:
        # gammainc is regularized (i.e. divided by gamma(a)) which is why we must multiply
        # by gamma(a) to get the true value of the integral.
        return gammainc(a, x) * gamma(a)


@register_formula([
    NumInput("x"),
    NumInput("alpha"),
    NumInput("beta")
], name="distributions.gamma")
def gamma_dist(x, a, b):
    """
    Evaluate the gamma distribution with parameters alpha and beta as defined in the textbook.
    """
    return stats.gamma.pdf(x, a, scale=b)


@register_formula([
    NumInput("lower bound", optional=True),
    NumInput("upper bound", optional=True),
    NumInput("alpha"),
    NumInput("beta")
], name="distributions.gamma.cumulative")
def gamma_dist(lower, upper, a, b):
    return find_distribution_area(stats.gamma, lower, upper, a, scale=b)


@register_formula([
    IntInput("v"),
    NumInput("alpha")
], name="distributions.chi2.inverse")
def inv_chi2_distribution(v, a):
    """
    Given an area 'a', return the value that if taken as a lower bound
    results in the chi-square distribution with v degrees of freedom having 'a' area above it.
    """
    return stats.chi2.ppf(1 - a, v)


@register_formula([
    IntInput("v"),
    NumInput("lower_bound", optional=True),
    NumInput("upper_bound", optional=True)
], name="distributions.chi2.cumulative")
def chi2_cuml(v, lower, upper):
    """
    Find the area between the lower and upper bounds and
    under the chi-squared distribution with v degrees of freedom.

    Bounds that aren't specified are taken at infinity.
    """
    return find_distribution_area(stats.chi2, lower, upper, v)


@register_formula([
    NumInput("v"),
    NumInput("alpha")
], name="distributions.t.inverse")
def inverse_t_dist(v, a):
    """
    Given an area 'a', return the value that if taken as a lower bound
    results in the student t distribution with v degrees of freedom having 'a' area above it.
    """
    return stats.t.ppf(1 - a, v)


@register_formula([
    IntInput("v"),
    NumInput("lower_bound", optional=True),
    NumInput("upper_bound", optional=True)
], name="distributions.t.cumulative")
def t_dist_cuml(v, lower, upper):
    """
    Find the area between the lower and upper bounds and
    under the t-distribution with v degrees of freedom.

    Bounds that aren't specified are taken at infinity.
    """
    return find_distribution_area(stats.t, lower, upper, v)


@register_formula([
    IntInput("v1"),
    IntInput("v2"),
    NumInput("lower_bound", optional=True),
    NumInput("upper_bound", optional=True)
], name="distributions.f.cumulative")
def f_dist_cuml(v1, v2, lower, upper):
    """
    Find the area under the F-distribution between
    the lower and upper bounds given that the
    F-distribution is comparing two chi-squared
    random variables with v1 and v2 degrees of freedom.

    Bounds that aren't specified are taken at infinity.
    """
    return find_distribution_area(stats.f, lower, upper, v1, v2)


@register_formula([
    IntInput("v1"),
    IntInput("v2"),
    NumInput("alpha")
], name="distributions.f.inverse")
def f_dist_inverse(v1, v2, a):
    """
    Given an area 'a', return the value that if taken as a lower bound
    results in the F-distribution with parameters v1 and v2 having 'a' area above it.
    """
    return stats.f.ppf(1 - a, v1, v2)


@register_formula((
        ListInput("x"),
        ListInput("y")
), name="sample.covariance_all_pairs")
def covarience_all_pairs(x, y):
    """
    Given two sets x and y, find the covarience assuming
    that any combination (x, y) is equally likely (happens
    when x and y are independent).
    """
    mean_x = mean(x)
    mean_y = mean(y)
    # Find of (xi - mean_x) * (yi - mean_y) for all possible combinations (x[i], y[j])
    return sum([(xi - mean_x) * (yj - mean_y) for xi in x for yj in y])


@register_formula((
        ListInput("x"),
        ListInput("y")
), name="sample.covariance_one_to_one")
def covarience_one_to_one(x, y):
    """
    Given two sets x and y of equal lengths, return
    the covarience assuming that x and y only occur in matching
    pairs (one-to-one relationship).
    """
    if len(x) != len(y):
        raise UserInputError("x and y must be one-to-one.")

    mean_x = mean(x)
    mean_y = mean(y)
    # Find of (xi - mean_x) * (yi - mean_y) for all pairs (xi, yi)
    return sum([(x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))])


def find_distribution_area(distribution: stats.rv_continuous, lower, upper, *args, **kwargs):
    """
    Find the area between the lower and upper bounds of a scipy.stats continuous random variable distribution.
    """
    # Verify that either lower or upper is specified
    if lower is None and upper is None:
        print("Lower and upper bounds can't both be None")
        raise UserInputError
    # If lower is not specified we want to find the area below upper
    if lower is None:
        return distribution.cdf(upper, *args, **kwargs)
    # If upper is not specified we want to find the are above lower
    if upper is None:
        return 1 - distribution.cdf(lower, *args, **kwargs)
    # Otherwise we find the area between the lower and upper bounds
    return distribution.cdf(upper, *args, **kwargs) - distribution.cdf(lower, *args, **kwargs)


if __name__ == "__main__":
    # Start the prompt used to evaluate the functions.
    launch_prompt()
