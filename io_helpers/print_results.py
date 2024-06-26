import numpy as np
from colorama import just_fix_windows_console
just_fix_windows_console()

# u_T: uncertainty of a target 3D coords
def simplified(test):
    """
    Print the results of the simplified test procedure.

    Args:
    - test (Simplified): An instance of the Simplified class containing the test results.
    """
    print('Results (simplified test procedure)')
    print(f'Allowed max deviation with alpha={test.alpha}: {str(round(test.max_dev*1e3, 3))}mm')
    for key, value in test.results.items():
        if abs(value) <= test.max_dev:
            check = '\033[92m■\033[0m'
        else:
            check = '\033[91m■\033[0m'
        print(f'{key}: {str(round(value*1e3, 3)).rjust(6)}mm {check}')

def full(test):
    """
    Print the results of the full test procedure.

    Args:
    - test (Full): An instance of the Full class containing the test results.
    """
    print('Results (full test procedure)')

    if test.std_s1_s2_differed:
        print(f'S1 and S2 have significantly different std deviations!')
        print(f'std_0_1: {round(test.std_0_1*1e3, 3)}mm\nstd_0_2: {round(test.std_0_2*1e3, 3)}mm')

    print(f'Standard uncertainty of the TLS for a point: {round(test.u_ISO_TLS*1e3, 3)}mm')

    print(f'Allowed max deviation with alpha={test.alpha}: {round(test.max_dev*1e3, 3)}mm')
    for key, value in test.results.items():
        if abs(value) <= test.max_dev:
            check = '\033[92m■\033[0m'
        else:
            check = '\033[91m■\033[0m'
        print(f'{key}: {str(round(value*1e3, 3)).rjust(6)}mm {check}')
