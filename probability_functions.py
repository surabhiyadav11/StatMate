import pandas as pd

def empirical_probability(df, condition_series):
    """
    Calculates Empirical Probability P(A).
    Condition series should be a boolean mask of the same length as df.
    """
    if df.empty:
        return 0, 0, 0
        
    total_eligible = len(df)
    satisfying_a = condition_series.sum()
    
    prob = satisfying_a / total_eligible if total_eligible > 0 else 0
    return prob, satisfying_a, total_eligible

def classification_probabilities(df, ridership_col, low_med_thresh, med_high_thresh):
    """
    Calculates P(Low), P(Medium), P(High) given user thresholds.
    """
    if df.empty:
        return {}
        
    total = len(df)
    
    low_mask = df[ridership_col] < low_med_thresh
    high_mask = df[ridership_col] >= med_high_thresh
    med_mask = ~(low_mask | high_mask)
    
    low_count = low_mask.sum()
    med_count = med_mask.sum()
    high_count = high_mask.sum()
    
    return {
        'P_Low': low_count / total,
        'P_Med': med_count / total,
        'P_High': high_count / total,
        'count_Low': low_count,
        'count_Med': med_count,
        'count_High': high_count,
        'total': total
    }

def conditional_probability(df, event_A_mask, event_B_mask):
    """
    Calculates P(A|B) = P(A AND B) / P(B)
    """
    if df.empty:
        return 0, 0, 0
        
    count_B = event_B_mask.sum()
    count_A_and_B = (event_A_mask & event_B_mask).sum()
    
    prob = count_A_and_B / count_B if count_B > 0 else 0
    
    return prob, count_A_and_B, count_B
