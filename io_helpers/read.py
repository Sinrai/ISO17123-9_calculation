import os
import sys

import pandas as pd

def read_path(config):
    """
    Read and process data files based on the configuration.

    Args:
    - config (Config): Configuration object containing parsed arguments and metadata.

    Returns:
    - result_df (pd.DataFrame): Processed DataFrame containing imported coordinates.
    """
    match config.format:
        case 'leica':
            files = sorted(os.listdir(config.data_directory))

            if not config.ff:
                print('Found the following files in the data directory:')
                for nr, f in enumerate(files):
                    print(f'[{nr}] {f}')
                order = input('Input file index and order of files to be used\nS1 (set 1-3) -> S2 (set 1-3)\nexample: 0,3\n> ')
                if not order:
                    print('Default order used')
                else:
                    order = [int(i) for i in order.split(',')]
                    files = [files[i] for i in order]
                print(80*'-')


            if config.ftp:
                naming = [('S1', 1), ('S1', 2), ('S1', 3), ('S2', 1), ('S2', 2), ('S2', 3)]
                if len(files) != 6:
                    print('Did not find 6 files for full test procedure')
                    sys.exit()
            if config.stp:
                naming = [('S1', 1), ('S2', 1)]
                if len(files) != 2:
                    print('Did not find 2 files for simplified test procedure')
                    sys.exit()

            print('Files to be used in the following order:')
            for nr, f in enumerate(files):
                print(f'[{nr}] {f}')
            print(80*'-')

            dfs = []
            for i, f in enumerate(files):
                df = pd.read_csv(os.path.join(config.data_directory, f), header=0, usecols=['T', 'X', 'Y', 'Z'], names=['T', 'X', 'Y', 'Z'])
                df[['S', 'w']] = naming[i]
                dfs.append(df)

            result_df = pd.concat(dfs, ignore_index=True)
            result_df = result_df.set_index(['S', 'w', 'T'])
            print('Imported coordinates:')
            print(result_df)
            print(80*'-')

            return result_df

