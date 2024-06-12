import numpy as np
import scipy.stats as stats

def question_a(s_hat_0, sigma_0, alpha, v):
    """
    Performs a hypothesis test for question a.

    This function calculates the critical value of the chi-squared distribution,
    compares it with the observed value, and returns a boolean indicating whether
    the null hypothesis should be rejected.

    See ISO 17123-9 sec 8.4.2 for more information.

    Args:
    - s_hat_0 (float): Observed standard deviation estimate.
    - sigma_0 (float): Hypothesized standard deviation.
    - alpha (float): Significance level of the test.
    - v (int): Degrees of freedom.

    Returns:
    - bool: True if the null hypothesis should be rejected, False otherwise.
    """
    X2 = stats.chi2.ppf(1 - alpha, v)
    print(X2)
    return s_hat_0/np.sqrt(2) <= sigma_0 * np.sqrt(X2/v)

def question_b(s_1, s_2, alpha, v_1, v_2):
    """
    Performs a hypothesis test for question b.

    This function calculates the critical values of the F-distribution,
    compares them with the observed ratio of variances, and returns a boolean
    indicating whether the null hypothesis should be rejected.

    See ISO 17123-9 sec 8.4.3 for more information.

    Args:
    - s_1 (float): Standard deviation of the first sample.
    - s_2 (float): Standard deviation of the second sample.
    - alpha (float): Significance level of the test.
    - v_1 (int): Degrees of freedom for the numerator.
    - v_2 (int): Degrees of freedom for the denominator.

    Returns:
    - bool: True if the null hypothesis should be rejected, False otherwise.
    """
    lower = 1/stats.f.ppf(1 - alpha/2, v_1, v_2)
    upper = stats.f.ppf(1 - alpha/2, v_1, v_2)

    return lower <= s_1**2/s_2**2 <= upper
