# ISO 17123-9 Calculation Automatisation

This is a CLI application to automate the calculatons needed for the simple and full test procedure according to the [ISO 17123-9:2018](https://www.iso.org/standard/68382.html) standard.
This repository does not describe or explain how to perform the test. For this purpose access to the ISO document is required.

This software was written as part of my BSc thesis.

## Installation

    git clone https://github.com/Sinrai/ISO17123-9_calculation.git
    cd ISO17123-9_calculation

    # Create environment (encouraged) venv, conda, etc
    pip install -r requirements.txt

(WIP) To create a PDF report, a working LaTeX processor needs to be installed additonally to pylatex.

    pip install pylatex

## Usage

Export target coordinates from the manufacurers processing software in a txt file.

    python iso17123-9.py [options]

#### Positional Arguments

* data_directory: Path to the files with target center coordinates.
* format: Which format the files are in. Currently supported: leica.

#### Options

* -h, --help: Show this help message and exit.
* -ff: Fast-Forward (no interactive shell, files are treated to be in the correct order).
* -ftp: Perform the full test procedure.
* -stp: Perform the simplified test procedure.
* -alpha ALPHA: Confidence interval (default: 0.05).

#### Simplified Test Procedure

* -u_t U_T: Uncertainty quantity u_t for a target's center (in mm).

#### Full Test Procedure

* -case CASE: Which case for a target uncertainty should be used (see 8.5.1 in the ISO document).
* -u_ms U_MS: Manufacturer specified target center uncertainty (in mm).
* -u_p U_P: Derived target center uncertainty from other sources (in mm).

#### Output Information

* -metadata METADATA: Path to metadata.yaml.
* -pdf PDF: Output Path to save generated PDF report.
* -csv CSV: Output Path to save results in CSV (appending if already existing).

### Examples

Perform Simplified Test Procedure

    python iso17123-9.py /path/to/data leica -stp -u_t 0.1

Perform Full Test Procedure with PDF report

    python iso17123-9.py /path/to/data leica -ftp -case A -u_ms 5 -metadata /path/to/metadata.yaml -pdf /path/to/report.pdf


## Supported formats

* (Leica) Cyclone Register 360
