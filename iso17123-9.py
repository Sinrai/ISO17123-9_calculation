#! /bin/env python

from io_helpers import read, print_results, csv
from computations import procedures
from config.config import Config

if __name__ == '__main__':
    config = Config()

    measurements = read.read_path(config)

    if config.ftp:  # full test procedure
        test = procedures.Full(measurements, config)
        print_results.full(test)
    if config.stp:  # simplified test procedure
        test = procedures.Simplified(measurements, config)
        print_results.simplified(test)

    if config.csv:
        csv.append_results(test, config)

    if config.pdf:
        from io_helpers import pdf
        pdf.generate_report(test, config)
