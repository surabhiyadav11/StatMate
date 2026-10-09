import scipy.stats as stats
import numpy as np
import pandas as pd

def calculate_binomial(n, p, k):
    """Calculates Binomial PMF and CDF for exact k."""
    pmf = stats.binom.pmf(k, n, p)
    cdf = stats.binom.cdf(k, n, p)
    return pmf, cdf

def generate_binomial_plot_data(n, p):
    x = np.arange(0, min(n + 1, 50))
    y = stats.binom.pmf(x, n, p)
    return pd.DataFrame({'x': x, 'PMF': y})

def calculate_poisson(lam, k):
    """Calculates Poisson PMF and CDF for exact k."""
    pmf = stats.poisson.pmf(k, lam)
    cdf = stats.poisson.cdf(k, lam)
    return pmf, cdf

def generate_poisson_plot_data(lam):
    x = np.arange(0, max(10, int(lam * 3)))
    y = stats.poisson.pmf(x, lam)
    return pd.DataFrame({'x': x, 'PMF': y})

def calculate_normal(mu, sigma, x):
    """Calculates Normal PDF and CDF."""
    pdf = stats.norm.pdf(x, mu, sigma)
    cdf = stats.norm.cdf(x, mu, sigma)
    return pdf, cdf

def generate_normal_plot_data(mu, sigma):
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
    y = stats.norm.pdf(x, mu, sigma)
    return pd.DataFrame({'x': x, 'PDF': y})

def calculate_exponential(scale, x):
    """Calculates Exponential PDF and CDF. scale = 1/lambda"""
    pdf = stats.expon.pdf(x, scale=scale)
    cdf = stats.expon.cdf(x, scale=scale)
    return pdf, cdf

def generate_exponential_plot_data(scale):
    x = np.linspace(0, scale * 5, 100)
    y = stats.expon.pdf(x, scale=scale)
    return pd.DataFrame({'x': x, 'PDF': y})

def calculate_uniform(a, b, x):
    """Calculates Uniform PDF and CDF."""
    pdf = stats.uniform.pdf(x, loc=a, scale=b-a)
    cdf = stats.uniform.cdf(x, loc=a, scale=b-a)
    return pdf, cdf

def generate_uniform_plot_data(a, b):
    # Add a bit of margin for the plot
    margin = (b - a) * 0.1
    x = np.linspace(a - margin, b + margin, 200)
    y = stats.uniform.pdf(x, loc=a, scale=b-a)
    return pd.DataFrame({'x': x, 'PDF': y})
