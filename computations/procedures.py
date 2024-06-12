import numpy as np
import scipy.stats as stats

from computations import stat_tests

combinations = [
    ('T1', 'T2'),
    ('T1', 'T3'),
    ('T1', 'T4'),
    ('T2', 'T3'),
    ('T2', 'T4'),
    ('T3', 'T4'),
]

def within_max_dev(results, max_dev):
    """
    Checks if all values in the results dictionary are within a specified maximum deviation.

    Args:
    - results (dict): A dictionary containing the results to be checked.
    - max_dev (float): The maximum allowed deviation.

    Returns:
    - bool: True if all values are within the maximum deviation, False otherwise.
    """
    return all(value < max_dev for value in results.values())


class Simplified:
    """
    Class representing the simplified test procedure.

    Attributes:
    - distances (dict): Dictionary containing calculated distances between pairs of measurements.
    - results (dict): Dictionary containing the calculated differences between pairs of distances.
    - alpha (float): Significance level for hypothesis testing.
    - u_t (float): Combined uncertainty based on the test procedure.
    - max_dev (float): Maximum allowed deviation for passing the test.
    - passed (bool): Flag indicating if the test passed or not.

    Methods:
    - __init__(self, data, config): Initializes the Simplified test procedure.
    """

    def __init__(self, data, config):
        """
        Initializes the Simplified test procedure.

        Args:
        - data (DataFrame): The data containing measurements.
        - config (Config): Configuration object containing parameters for the test.

        Initializes distances, results, alpha, u_t, max_dev, and passed attributes.
        """
        self.distances = dict()
        for station in ['S1', 'S2']:
            for i, j in combinations:
                self.distances[(station, i, j)] = np.linalg.norm(data.loc[(station, 1, j)] - data.loc[(station, 1, i)])

        self.results = {
            'delta_1_2': self.distances[('S1', 'T1', 'T2')] - self.distances[('S2', 'T1', 'T2')],
            'delta_1_3': self.distances[('S1', 'T1', 'T3')] - self.distances[('S2', 'T1', 'T3')],
            'delta_1_4': self.distances[('S1', 'T1', 'T4')] - self.distances[('S2', 'T1', 'T4')],
            'delta_2_3': self.distances[('S1', 'T2', 'T3')] - self.distances[('S2', 'T2', 'T3')],
            'delta_2_4': self.distances[('S1', 'T2', 'T4')] - self.distances[('S2', 'T2', 'T4')],
            'delta_3_4': self.distances[('S1', 'T3', 'T4')] - self.distances[('S2', 'T3', 'T4')],
        }

        self.alpha = config.alpha
        self.u_t = config.u_t
        self.max_dev = stats.norm.ppf(1-self.alpha/2)*2*self.u_t
        self.passed = within_max_dev(self.results, self.max_dev)


class Full:
    """
    Class representing the full test procedure.

    This class calculates distances between pairs of measurements for two stations (S1 and S2)
    and performs more extensive statistical tests based on the configuration parameters.

    Attributes:
    - distances (dict): Dictionary containing calculated distances between pairs of measurements.
    - single_distances (dict): Dictionary containing lists of individual distances for each pair of measurements.
    - results (dict): Dictionary containing the calculated differences between pairs of distances.
    - alpha (float): Significance level for hypothesis testing.
    - residuals (dict): Dictionary containing residuals after subtracting single distances from average distances.
    - std_0_1 (float): Standard deviation of residuals for station S1.
    - std_0_2 (float): Standard deviation of residuals for station S2.
    - std_0 (float): Combined standard deviation based on the test procedure.
    - std_s1_s2_differed (bool): Flag indicating if standard deviations for stations S1 and S2 differed significantly.
    - std_mean_0 (float): Standard deviation of mean distances.
    - u_ISO_TLS (float): Combined uncertainty based on the ISO and TLS measurements.
    - u_ms (float): Uncertainty based on the measurement standard (case A).
    - u_p (float): Uncertainty based on the precision (case B).
    - max_dev (float): Maximum allowed deviation for passing the test.
    - passed (bool): Flag indicating if the test passed or not.

    Methods:
    - __init__(self, data, config): Initializes the Full test procedure.
    """

    def __init__(self, data, config):
        """
        Initializes the Full test procedure.

        Args:
        - data (DataFrame): The data containing measurements.
        - config (Config): Configuration object containing parameters for the test.

        Initializes distances, single_distances, results, alpha, residuals, std_0_1, std_0_2,
        std_0, std_s1_s2_differed, std_mean_0, u_ISO_TLS, u_ms, u_p, max_dev, and passed attributes.
        """
        self.distances = dict()
        self.single_distances = dict()
        for station in ['S1', 'S2']:
            for i, j in combinations:
                single_dist = []
                for w in [1, 2, 3]:
                    single_dist.append(np.linalg.norm(data.loc[(station, w, j)] - data.loc[(station, w, i)]))
                self.distances[(station, i, j)] = np.mean(single_dist)
                self.single_distances[(station, i, j)] = single_dist

        self.results = {
            'delta_1_2': self.distances[('S1', 'T1', 'T2')] - self.distances[('S2', 'T1', 'T2')],
            'delta_1_3': self.distances[('S1', 'T1', 'T3')] - self.distances[('S2', 'T1', 'T3')],
            'delta_1_4': self.distances[('S1', 'T1', 'T4')] - self.distances[('S2', 'T1', 'T4')],
            'delta_2_3': self.distances[('S1', 'T2', 'T3')] - self.distances[('S2', 'T2', 'T3')],
            'delta_2_4': self.distances[('S1', 'T2', 'T4')] - self.distances[('S2', 'T2', 'T4')],
            'delta_3_4': self.distances[('S1', 'T3', 'T4')] - self.distances[('S2', 'T3', 'T4')],
        }

        self.alpha = config.alpha

        self.residuals = dict()
        for station in ['S1', 'S2']:
            for i, j in combinations:
                self.residuals[(station, i, j)] = self.distances[(station, i, j)] - np.array(self.single_distances[(station, i, j)])
        Omega_S1 = np.sum(np.concatenate((
                                self.residuals[('S1', 'T1', 'T2')],
                                self.residuals[('S1', 'T1', 'T3')],
                                self.residuals[('S1', 'T1', 'T4')],
                                self.residuals[('S1', 'T2', 'T3')],
                                self.residuals[('S1', 'T2', 'T4')],
                                self.residuals[('S1', 'T3', 'T4')],
                        ))**2)
        Omega_S2 = np.sum(np.concatenate((
                                self.residuals[('S2', 'T1', 'T2')],
                                self.residuals[('S2', 'T1', 'T3')],
                                self.residuals[('S2', 'T1', 'T4')],
                                self.residuals[('S2', 'T2', 'T3')],
                                self.residuals[('S2', 'T2', 'T4')],
                                self.residuals[('S2', 'T3', 'T4')],
                        ))**2)

        self.std_0_1 = np.sqrt(Omega_S1/12)
        self.std_0_2 = np.sqrt(Omega_S2/12)

        # Statistical test if std_0_1 and std_0_2 differ
        if stat_tests.question_b(self.std_0_1, self.std_0_2, self.alpha, 12, 12):
            self.std_0 = np.sqrt((Omega_S1+Omega_S2)/24)
            self.std_s1_s2_differed = False
        else:
            self.std_0 = (self.std_0_1 + self.std_0_2)/2
            self.std_s1_s2_differed = True

        d_mean_1_2 = (self.distances[('S1', 'T1', 'T2')] + self.distances[('S2', 'T1', 'T2')])/2
        d_mean_1_3 = (self.distances[('S1', 'T1', 'T3')] + self.distances[('S2', 'T1', 'T3')])/2
        d_mean_1_4 = (self.distances[('S1', 'T1', 'T4')] + self.distances[('S2', 'T1', 'T4')])/2
        d_mean_2_3 = (self.distances[('S1', 'T2', 'T3')] + self.distances[('S2', 'T2', 'T3')])/2
        d_mean_2_4 = (self.distances[('S1', 'T2', 'T4')] + self.distances[('S2', 'T2', 'T4')])/2
        d_mean_3_4 = (self.distances[('S1', 'T3', 'T4')] + self.distances[('S2', 'T3', 'T4')])/2

        Omega_dist = np.sum(np.concatenate((
                                d_mean_1_2 - self.single_distances[('S1', 'T1', 'T2')],
                                d_mean_1_3 - self.single_distances[('S1', 'T1', 'T3')],
                                d_mean_1_4 - self.single_distances[('S1', 'T1', 'T4')],
                                d_mean_2_3 - self.single_distances[('S1', 'T2', 'T3')],
                                d_mean_2_4 - self.single_distances[('S1', 'T2', 'T4')],
                                d_mean_3_4 - self.single_distances[('S1', 'T3', 'T4')],
                                d_mean_1_2 - self.single_distances[('S2', 'T1', 'T2')],
                                d_mean_1_3 - self.single_distances[('S2', 'T1', 'T3')],
                                d_mean_1_4 - self.single_distances[('S2', 'T1', 'T4')],
                                d_mean_2_3 - self.single_distances[('S2', 'T2', 'T3')],
                                d_mean_2_4 - self.single_distances[('S2', 'T2', 'T4')],
                                d_mean_3_4 - self.single_distances[('S2', 'T3', 'T4')],
                            ))**2)

        self.std_mean_0 = np.sqrt(Omega_dist/30)
        self.u_ISO_TLS = self.std_mean_0/np.sqrt(2)

        match config.case.upper():
            case 'A':
                self.u_ms = config.u_ms
                self.u_t = self.u_ms
            case 'B':
                self.u_p = config.u_p
                self.u_t = np.sqrt(self.u_ISO_TLS**2 + self.u_p**2)
            case 'C':
                self.u_t = self.u_ISO_TLS

        self.max_dev = stats.norm.ppf(1-self.alpha/2)*2*self.u_t/np.sqrt(3)
        self.passed = within_max_dev(self.results, self.max_dev)
