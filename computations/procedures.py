import numpy as np

combinations = [
    ('T1', 'T2'),
    ('T1', 'T3'),
    ('T1', 'T4'),
    ('T2', 'T3'),
    ('T2', 'T4'),
    ('T3', 'T4'),
]

def simplified(data):
    distances = dict()
    for station in ['S1', 'S2']:
        for i, j in combinations:
            distances[(station, i, j)] = np.linalg.norm(data.loc[(station, 1, j)] - data.loc[(station, 1, i)])

    results = {
        'delta_1_2': distances[('S1', 'T1', 'T2')] - distances[('S2', 'T1', 'T2')],
        'delta_1_3': distances[('S1', 'T1', 'T3')] - distances[('S2', 'T1', 'T3')],
        'delta_1_4': distances[('S1', 'T1', 'T4')] - distances[('S2', 'T1', 'T4')],
        'delta_2_3': distances[('S1', 'T2', 'T3')] - distances[('S2', 'T2', 'T3')],
        'delta_2_4': distances[('S1', 'T2', 'T4')] - distances[('S2', 'T2', 'T4')],
        'delta_3_4': distances[('S1', 'T3', 'T4')] - distances[('S2', 'T3', 'T4')],
    }
    return distances, results

def full(data):
    distances = dict()
    single_distances = dict()
    for station in ['S1', 'S2']:
        for i, j in combinations:
            single_dist = []
            for w in [1, 2, 3]:
                single_dist.append(np.linalg.norm(data.loc[(station, w, j)] - data.loc[(station, w, i)]))
            distances[(station, i, j)] = np.mean(single_dist)
            single_distances[(station, i, j)] = single_dist

    results = {
        'delta_1_2': distances[('S1', 'T1', 'T2')] - distances[('S2', 'T1', 'T2')],
        'delta_1_3': distances[('S1', 'T1', 'T3')] - distances[('S2', 'T1', 'T3')],
        'delta_1_4': distances[('S1', 'T1', 'T4')] - distances[('S2', 'T1', 'T4')],
        'delta_2_3': distances[('S1', 'T2', 'T3')] - distances[('S2', 'T2', 'T3')],
        'delta_2_4': distances[('S1', 'T2', 'T4')] - distances[('S2', 'T2', 'T4')],
        'delta_3_4': distances[('S1', 'T3', 'T4')] - distances[('S2', 'T3', 'T4')],
    }
    return distances, single_distances, results
