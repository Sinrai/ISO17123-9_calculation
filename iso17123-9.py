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


    args = parser.parse_args()

    # Validation
    if not os.path.exists(args.target_path):
        print('Invalid target_path!')
        sys.exit()

    if args.manufacturer.lower() not in supported_formats:
        print('Unsupported manufacturer!')
        newline = '\n  '
        print(f'Supported manufacturers are: {newline}{newline.join(supported_formats)}')
        sys.exit()

    print(80*'-')
    print('ISO 17123-9 Calculation Automatisation')
    print(80*'-')
    print(f'Target path:         {args.target_path}')
    print(f'Manufacturer format: {args.manufacturer}')
    print(80*'-')

    measurements = read.read_path(args.target_path, args.manufacturer, args.ff, args.full)

    if args.full:
        distances, single_distances, results = procedures.full(measurements)
        print_results.full(args.alpha, distances, single_distances, results)
    else:
        distances, results = procedures.simplified(measurements)
        print_results.simplified(args.alpha, 0.0012, distances, results)
