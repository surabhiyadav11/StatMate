import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path to import logic modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stats_functions import calculate_central_tendency, calculate_range_measures, calculate_dispersion, calculate_correlation
from probability_functions import empirical_probability, classification_probabilities, conditional_probability
import distribution_functions as dist

class TestCalculations(unittest.TestCase):

    def setUp(self):
        # Create a controlled dataframe for testing
        self.df = pd.DataFrame({
            'Ridership': [10, 20, 20, 30, 40, 50, 100], # Mean: 38.57, Median: 30, Mode: 20
            'Station': ['A', 'A', 'B', 'B', 'A', 'C', 'C'],
            'Date': pd.date_range(start='2025-01-01', periods=7),
            'Hour': [1, 2, 1, 2, 3, 1, 2]
        })
        self.series = self.df['Ridership']

    def test_central_tendency(self):
        mean, median, modes = calculate_central_tendency(self.series)
        self.assertAlmostEqual(mean, 270/7)
        self.assertEqual(median, 30)
        self.assertEqual(modes, [20])

    def test_range_measures(self):
        min_v, max_v, range_v = calculate_range_measures(self.series)
        self.assertEqual(min_v, 10)
        self.assertEqual(max_v, 100)
        self.assertEqual(range_v, 90)

    def test_dispersion(self):
        disp = calculate_dispersion(self.series)
        self.assertEqual(disp['n'], 7)
        self.assertAlmostEqual(disp['pop_var'], np.var(self.series, ddof=0))
        self.assertAlmostEqual(disp['samp_var'], np.var(self.series, ddof=1))
        
        # Test quartiles
        self.assertEqual(disp['q2'], 30)
        
        # IQR = Q3(45) - Q1(20) = 25
        self.assertEqual(disp['iqr'], 25)

    def test_empirical_prob(self):
        cond = self.series >= 30
        prob, sat, tot = empirical_probability(self.df, cond)
        self.assertEqual(tot, 7)
        self.assertEqual(sat, 4) # 30, 40, 50, 100
        self.assertEqual(prob, 4/7)

    def test_classification_prob(self):
        probs = classification_probabilities(self.df, 'Ridership', 25, 45)
        # Low < 25: 10, 20, 20 (3)
        # Med 25-45: 30, 40 (2)
        # High >= 45: 50, 100 (2)
        self.assertEqual(probs['count_Low'], 3)
        self.assertEqual(probs['count_Med'], 2)
        self.assertEqual(probs['count_High'], 2)
        self.assertAlmostEqual(probs['P_Low'] + probs['P_Med'] + probs['P_High'], 1.0)

    def test_conditional_prob(self):
        mask_a = self.series >= 40 # 40, 50, 100
        mask_b = self.df['Station'] == 'A' # indices 0(10), 1(20), 4(40)
        prob, count_ab, count_b = conditional_probability(self.df, mask_a, mask_b)
        self.assertEqual(count_b, 3)
        self.assertEqual(count_ab, 1) # only index 4 (40) is in both
        self.assertEqual(prob, 1/3)

    def test_distributions(self):
        pmf, cdf = dist.calculate_binomial(10, 0.5, 5)
        self.assertTrue(0 <= pmf <= 1)
        self.assertTrue(0 <= cdf <= 1)
        
        pdf, cdf = dist.calculate_normal(0, 1, 0)
        self.assertAlmostEqual(cdf, 0.5)

    def test_empty_series(self):
        empty_s = pd.Series([], dtype=float)
        mean, med, mod = calculate_central_tendency(empty_s)
        self.assertIsNone(mean)
        self.assertIsNone(med)
        self.assertEqual(mod, [])

if __name__ == '__main__':
    unittest.main()
