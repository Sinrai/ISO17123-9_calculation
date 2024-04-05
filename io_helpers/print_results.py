import numpy as np
import scipy.stats as stats

from computations.procedures import combinations
from computations import stat_tests

# u_T: uncertainty of a target 3D coords
def simplified(alpha, u_T, distances, results):
    print('Results (simplified test procedure)')
    max_dev = stats.norm.ppf(1-alpha/2)*2*u_T
    print(f'Allowed max deviation with alpha={alpha}: {str(round(max_dev*1e3, 3))}mm')
    for key, value in results.items():
        if abs(value) <= max_dev:
            test = '\033[92m■\033[0m'
        else:
            test = '\033[91m■\033[0m'
        print(f'{key}: {str(round(value*1e3, 3)).rjust(6)}mm {test}')

def full(alpha, distances, single_distances, results):
    print('Results (full test procedure)')

    residuals = dict()
    for station in ['S1', 'S2']:
        for i, j in combinations:
            residuals[(station, i, j)] = distances[(station, i, j)] - np.array(single_distances[(station, i, j)])
    Omega_S1 = np.sum(np.concatenate((
                            residuals[('S1', 'T1', 'T2')],
                            residuals[('S1', 'T1', 'T3')],
                            residuals[('S1', 'T1', 'T4')],
                            residuals[('S1', 'T2', 'T3')],
                            residuals[('S1', 'T2', 'T4')],
                            residuals[('S1', 'T3', 'T4')],
                      ))**2)
    Omega_S2 = np.sum(np.concatenate((
                            residuals[('S2', 'T1', 'T2')],
                            residuals[('S2', 'T1', 'T3')],
                            residuals[('S2', 'T1', 'T4')],
                            residuals[('S2', 'T2', 'T3')],
                            residuals[('S2', 'T2', 'T4')],
                            residuals[('S2', 'T3', 'T4')],
                      ))**2)

    std_0_1 = np.sqrt(Omega_S1/12)
    std_0_2 = np.sqrt(Omega_S2/12)
    std_0 = np.sqrt((Omega_S1+Omega_S2)/24)

    # Statistical test if std_0_1 and std_0_2 differ
    if stat_tests.question_b(std_0_1, std_0_2, alpha, 12, 12):
        std_0 = np.sqrt((Omega_S1+Omega_S2)/24)
    else:
        print(f'S1 and S2 have significantly different std deviations!')
        print(f'std_0_1: {std_0_1}\nstd_0_2: {std_0_2}')
        std_0 = (std_0_1 + std_0_2)/2

    precision_3d = std_0/np.sqrt(2)
    #print(precision_3d*1e3)

    d_mean_1_2 = (distances[('S1', 'T1', 'T2')] + distances[('S2', 'T1', 'T2')])/2
    d_mean_1_3 = (distances[('S1', 'T1', 'T3')] + distances[('S2', 'T1', 'T3')])/2
    d_mean_1_4 = (distances[('S1', 'T1', 'T4')] + distances[('S2', 'T1', 'T4')])/2
    d_mean_2_3 = (distances[('S1', 'T2', 'T3')] + distances[('S2', 'T2', 'T3')])/2
    d_mean_2_4 = (distances[('S1', 'T2', 'T4')] + distances[('S2', 'T2', 'T4')])/2
    d_mean_3_4 = (distances[('S1', 'T3', 'T4')] + distances[('S2', 'T3', 'T4')])/2

    Omega_dist = np.sum(np.concatenate((
                            d_mean_1_2 - single_distances[('S1', 'T1', 'T2')],
                            d_mean_1_3 - single_distances[('S1', 'T1', 'T3')],
                            d_mean_1_4 - single_distances[('S1', 'T1', 'T4')],
                            d_mean_2_3 - single_distances[('S1', 'T2', 'T3')],
                            d_mean_2_4 - single_distances[('S1', 'T2', 'T4')],
                            d_mean_3_4 - single_distances[('S1', 'T3', 'T4')],
                            d_mean_1_2 - single_distances[('S2', 'T1', 'T2')],
                            d_mean_1_3 - single_distances[('S2', 'T1', 'T3')],
                            d_mean_1_4 - single_distances[('S2', 'T1', 'T4')],
                            d_mean_2_3 - single_distances[('S2', 'T2', 'T3')],
                            d_mean_2_4 - single_distances[('S2', 'T2', 'T4')],
                            d_mean_3_4 - single_distances[('S2', 'T3', 'T4')],
                      ))**2)

    std_mean_0 = np.sqrt(Omega_dist/30)
    u_ISO_TLS = std_mean_0/np.sqrt(2)
    print(f'Standard uncertainty of the TLS for a point: {round(u_ISO_TLS*1e3, 3)}mm')

    test_case = 'A'
    # Case A: get uT from manuf
    # Case B: sqrt(u_ISO_TLS**2+u_p**2)
    # Case C:
    match test_case:
        case 'A':
            u_T = 0.004
        case 'B':
            # sqrt(u_ISO_TLS**2+u_p**2)
            u_T = np.sqrt(u_ISO_TLS**2 + u_p**2)
        case 'C':
            # u_p = 0, -> u_ISO_TLS
            u_T = u_ISO_TLS

    max_dev = stats.norm.ppf(1-alpha/2)*2*u_T/np.sqrt(3)
    print(f'Allowed max deviation with alpha={alpha}: {round(max_dev*1e3, 3)}mm')
    for key, value in results.items():
        if abs(value) <= max_dev:
            test = '\033[92m■\033[0m'
        else:
            test = '\033[91m■\033[0m'
        print(f'{key}: {str(round(value*1e3, 3)).rjust(6)}mm {test}')

    stat_tests.question_b(1,1,0.05, 12,12)
