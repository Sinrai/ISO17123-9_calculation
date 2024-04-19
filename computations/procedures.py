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


class Simplified:
    def __init__(self, data, u_T, alpha=0.05):
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

        self.alpha = alpha
        self.u_T = u_T
        self.max_dev = stats.norm.ppf(1-self.alpha/2)*2*self.u_T


class Full:
    def __init__(self, data, test_case, u_ms, u_p, alpha):
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

        self.alpha = alpha
        self.u_ms = u_ms
        self.u_p = u_p

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

        #precision_3d = std_0/np.sqrt(2)
        #print(precision_3d*1e3)

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

        match test_case.upper():
            case 'A':
                self.u_T = self.u_ms
            case 'B':
                self.u_T = np.sqrt(self.u_ISO_TLS**2 + self.u_p**2)
            case 'C':
                self.u_T = self.u_ISO_TLS

        self.max_dev = stats.norm.ppf(1-self.alpha/2)*2*self.u_T/np.sqrt(3)
