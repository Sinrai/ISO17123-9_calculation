import argparse
import os
import sys
import yaml
from datetime import datetime

supported_formats = ['leica']
header = 'ISO 17123-9 Calculation Automatisation, see chapters 7.5 and 8.3 of the standard'
metadata_keys = {'device','manufacturer','serial_number','FW_version','operator','datetime','temp','humidity','pressure','comment'}

# Helper class to get all additional information, either via cmd line, yaml file or interactive CLI
class Config:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
                        prog = 'iso17123-9.py',
                        description = header)

        self.parser.add_argument('data_directory', help='path to the files with target center coordinates')
        self.parser.add_argument('format', help=f'Which format the files are in. Currently supported: {", ".join(supported_formats)}')
        self.parser.add_argument('-ff', action='store_true', help='Fast-Forward (no interactive shell, files are treated to be in the correct order)')
        self.parser.add_argument('-ftp', action='store_true', help='Perform the full test procedure')
        self.parser.add_argument('-stp', action='store_true', help='Perform the simplified test procedure')
        self.parser.add_argument('-alpha', type=float, default=0.05, help='Confidence interval (default: 0.05)')

        simple_group = self.parser.add_argument_group('Simplified test procedure')
        simple_group.add_argument('-u_t', type=float, help='Uncertainty quantity u_t for a targets center (in mm)')

        full_group = self.parser.add_argument_group('Full test procedure')
        full_group.add_argument('-case', help='Which case for a target uncertainty should be used (see 8.5.1 in the ISO document)')
        full_group.add_argument('-u_ms', type=float, help='Manufacturer specified target center uncertainty (in mm)')
        full_group.add_argument('-u_p', type=float, help='Derived target center uncertainty from other sources (in mm)')

        output_group = self.parser.add_argument_group('Output information')
        output_group.add_argument('-metadata', help='Path to metadata.yaml')
        output_group.add_argument('-pdf', help='Output Path to save generated pdf report')
        output_group.add_argument('-csv', help='Output Path to save results in csv (appending if already existing)')

        self.args = self.parser.parse_args()
        print(header, end='\n\n')

        # Validation and extra input

        self.data_directory = self.args.data_directory
        if not os.path.exists(self.data_directory):
            print('Invalid data directory!')
            sys.exit()

        self.format = self.args.format.lower()
        if self.format not in supported_formats:
            print(f'Unsupported format! ({self.format})')
            print(f'Supported formats are: \n  {'\n  '.join(supported_formats)}')
            sys.exit()

        self.metadata_path = self.args.metadata
        if self.metadata_path and not os.path.exists(self.metadata_path):
            print('Invalid path to metadata information (yaml file)!')
            sys.exit()

        if self.args.pdf:
            try:
                __import__('pylatex')
            except ImportError:
                print("PyLaTeX not installed, can't create pdf report!")
                sys.exit()

        self.ff = self.args.ff

        self.ftp = self.args.ftp
        self.stp = self.args.stp
        if self.ftp and self.stp:
            print('Can only do one test procedure!')
            print('Set either -ftp or -stp, but not both')
            sys.exit()
        if not self.ftp and not self.stp:
            print('Specify full or simplified test procedure:')
            print('(either "ftp" or "stp")')
            test_proc = input('> ')
            if test_proc == 'ftp':
                self.ftp = True
            elif test_proc == 'stp':
                self.stp = True
            else:
                print('Invalid test procedure!')
                sys.exit()

        self.alpha = self.args.alpha
        if not (0 < self.alpha < 1):
            print(f'Invalid confidence interval! ({self.alpha})')
            print('Must be between 0 and 1 (default 0.05)')
            sys.exit()

        if self.stp:
            if not self.args.u_t:
                print('No uncertainty quantity u_t for a targets center was specified!')
                print('In case of the simple test procedure this has to specified (in mm)')
                try:
                    self.u_t = float(input('> '))/1e3
                except ValueError:
                    print('Invalid float value')
                    sys.exit()
            else:
                self.u_t = self.args.u_t/1e3
            if self.u_t <= 0:
                print("Uncertainty quantity u_t for a targets center can't be negative!")
                sys.exit()

        if self.ftp:
            if not self.args.case:
                print('Specify case for the uncertainty of a targets center, see 8.5.1 in the ISO document')
                print('Must be either "A", "B" or "C"')
                self.case = input('> ').lower()
            else:
                self.case = self.args.case.lower()
            if self.case not in 'abc':
                print('Invalid case for the uncertainty of a targets center! Must be A, B or C, see 8.5.1 in the ISO document')
                sys.exit()

            match self.case:
                case 'a':
                    if not self.args.u_ms:
                        print('Case A: Specify target center uncertainty (u_ms) as specified by the manufacturer (in mm)')
                        try:
                            self.u_ms = float(input('> '))/1e3
                        except ValueError:
                            print('Invalid float value')
                            sys.exit()
                    else:
                        self.u_ms = self.args.u_ms/1e3
                    if self.u_ms <= 0:
                        print("Uncertainty quantity u_ms for a targets center can't be negative!")
                        sys.exit()
                case 'b':
                    if not self.args.u_p:
                        print('Case B: Derived target center uncertainty (u_p) from other sources (in mm)')
                        try:
                            self.u_p = float(input('> '))/1e3
                        except ValueError:
                            print('Invalid float value')
                            sys.exit()
                    else:
                        self.u_p = self.args.u_p/1e3
                    if self.u_p <= 0:
                        print("Uncertainty quantity u_p for a targets center can't be negative!")
                        sys.exit()
                case 'c':
                    pass # Special case of B with u_p = 0

        if self.metadata_path:
            with open(self.metadata_path, 'r') as f:
                self.metadata = yaml.safe_load(f)['metadata']
        else:
            self.metadata = dict()
        if not metadata_keys.issubset(self.metadata.keys()):
            if not self.ff:
                print('Some Metadate information is missing! Do you want to add them? (y/yes)')
                q = input('> ')
                if q.lower() in ['y', 'yes']:
                    for key in metadata_keys:
                        if key not in self.metadata.keys():
                            self.metadata[key] = input(f'  {key}: ')
            for key in metadata_keys:
                if key not in self.metadata.keys():
                    self.metadata[key] = ''

        self.pdf = self.args.pdf
        if self.pdf:
            dirs = os.path.dirname(self.pdf)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            if os.path.exists(self.pdf):
                pass #  File already exists, will be overwritten

        self.csv = self.args.csv
        if self.csv:
            dirs = os.path.dirname(self.csv)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            if os.path.exists(self.csv):
                pass #  File already exists, will be appended
            else:
                # Creating new empty file with header
                with open(self.csv, 'w') as f:
                    f.write('device,manufacturer,serial_number,FW_version,operator,datetime_test,datetime_eval,temp,humidity,pressure,u_TLS_ISO,passed,alpha,u_t,test_procedure,comment\n')

        self.current_dt = datetime.now().strftime("%Y-%m-%d %H:%M")
