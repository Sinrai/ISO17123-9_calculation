import numpy as np
import scipy.stats as stats

def question_a(s_hat_0, sigma_0, alpha, v):
    X2 = stats.chi2.ppf(1 - alpha, v)
    print(X2)
    return s_hat_0/np.sqrt(2) <= sigma_0 * np.sqrt(X2/v)

def question_b(s_1, s_2, alpha, v_1, v_2):
    lower = 1/stats.f.ppf(1 - alpha/2, v_1, v_2)
    upper = stats.f.ppf(1 - alpha/2, v_1, v_2)

    return lower <= s_1**2/s_2**2 <= upper
