#! /bin/env python

import argparse
import os
import sys

from io_helpers import read, print_results
from computations import procedures

supported_formats = ['leica']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog = 'iso17123-9.py',
                        description = 'ISO 17123-9 Calculation Automatisation, see chapters 7.5 and 8.3 of the standard')

    parser.add_argument('target_path', help='path to the files with target coordinates')
    parser.add_argument('manufacturer', help='which format the files are in')
    parser.add_argument('-ff', action='store_true', help='Fast-Forward (no interactive shell, files are treated to be in the correct order)')
    parser.add_argument('-full', action='store_true', help='Perform the full test procedure (default simplified)')
    parser.add_argument('-alpha', type=float, default=0.05, help='confidence interval (default: 0.05)')

    simple_group = parser.add_argument_group('Simplified test procedure')
    simple_group.add_argument('-u_t', type=float, required='-full' not in sys.argv, help='uncertainty quantity u_T for a targets center')

    full_group = parser.add_argument_group('Full test procedure')
    full_group.add_argument('-case', required='-full' in sys.argv, help='Which case for a target uncertainty should be used (see 8.5.1 in the ISO document)')
    full_group.add_argument('-u_ms', type=float, required=any(arg.lower() == 'a' for arg in sys.argv), help='Manufacturer specified target center uncertainty (Case A)')
    full_group.add_argument('-u_p', type=float, required=any(arg.lower() == 'b' for arg in sys.argv), help='derived target center uncertainty from other sources (Case B)')

    args = parser.parse_args()
    print(sys.argv)

    # Validation
    if not os.path.exists(args.target_path):
        print('Invalid target_path!')
        sys.exit()

    if args.manufacturer.lower() not in supported_formats:
        print('Unsupported manufacturer!')
        newline = '\n  '
        print(f'Supported manufacturers are: {newline}{newline.join(supported_formats)}')
        sys.exit()

    if args.full and args.case.lower() not in 'abc':
        print('Invalid case! Must be A, B or C, see 8.5.1 in the ISO document')
        sys.exit()

    print(80*'-')
    print('ISO 17123-9 Calculation Automatisation')
    print(80*'-')
    print(f'Target path:         {args.target_path}')
    print(f'Manufacturer format: {args.manufacturer}')
    print(80*'-')

    measurements = read.read_path(args.target_path, args.manufacturer, args.ff, args.full)

    if args.full:
        test = procedures.Full(measurements, test_case=args.case, u_ms=args.u_ms, u_p=args.u_p, alpha=args.alpha)
        print_results.full(test)
    else:
        test = procedures.Simplified(measurements, u_T=args.u_t, alpha=args.alpha)
        print_results.simplified(test)
