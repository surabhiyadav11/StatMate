import pandas as pd
import numpy as np

def calculate_central_tendency(series):
    """Calculates mean, median, and mode(s)."""
    if series.empty:
        return None, None, []
    
    mean = series.mean()
    median = series.median()
    # modes can be multiple
    modes = series.mode().tolist()
    
    return mean, median, modes

def calculate_range_measures(series):
    """Calculates min, max, and range."""
    if series.empty:
        return None, None, None
        
    min_val = series.min()
    max_val = series.max()
    range_val = max_val - min_val
    
    return min_val, max_val, range_val

def calculate_dispersion(series):
    """Calculates variance, std dev (pop and sample), CV, quartiles, IQR, and outliers."""
    if series.empty:
        return {}
        
    n = len(series)
    
    # Population (ddof=0)
    pop_var = series.var(ddof=0)
    pop_std = series.std(ddof=0)
    
    # Sample (ddof=1)
    if n > 1:
        samp_var = series.var(ddof=1)
        samp_std = series.std(ddof=1)
    else:
        samp_var = None
        samp_std = None
        
    mean_val = series.mean()
    cv = (pop_std / mean_val * 100) if mean_val != 0 else None
    
    q1 = series.quantile(0.25)
    q2 = series.quantile(0.50) # median
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outliers = series[(series < lower_bound) | (series > upper_bound)].tolist()
    
    return {
        'n': n,
        'pop_var': pop_var,
        'pop_std': pop_std,
        'samp_var': samp_var,
        'samp_std': samp_std,
        'cv': cv,
        'q1': q1,
        'q2': q2,
        'q3': q3,
        'iqr': iqr,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'outliers': outliers,
        'outlier_count': len(outliers)
    }

def calculate_correlation(df, col1, col2):
    """Calculates Pearson correlation between two columns."""
    valid_df = df.dropna(subset=[col1, col2])
    n = len(valid_df)
    
    if n < 2:
        return None, n
        
    corr = valid_df[col1].corr(valid_df[col2])
    return corr, n
