from pylatex import Document, Section, Subsection, Command, Tabular, MultiColumn, Math
from pylatex.utils import NoEscape, bold, italic
from pylatex.package import Package

metadata_keys = {'device','manufacturer','serial_number','FW_version','operator','datetime','temp','humidity','pressure','comment'}

class PDF_report(Document):
    """
    PDF Report class for ISO 17123-9 test results.

    Args:
    - test (object): Instance of the test results (either Simplified or Full).
    - config (object): Configuration object containing metadata and test parameters.
    """
    def __init__(self, test, config):
        geometry_options = {'tmargin': '1.5cm', 'lmargin': '1.5cm', 'rmargin': '1.5cm', 'bmargin': '1.5cm'}
        super().__init__('article', geometry_options=geometry_options, document_options=['a4paper'])

        self.test = test
        self.config = config

        self.packages.append(Package('graphicx'))
        self.packages.append(Package('geometry'))
        self.packages.append(Package('multicol'))
        self.packages.append(Package('xcolor'))
        self.packages.append(Package('tikz'))
        # self.packages.append(Package('fancyhdr'))

        self.preamble.append(Command('title', Command('textbf', f'ISO 17123-9 test report')))
        self.preamble.append(Command('date', config.current_dt))
        self.preamble.append(Command('pagenumbering', 'gobble'))

        # self.preamble.append(Command('pagestyle', 'fancy'))
        # self.preamble.append(Command('fancyhf', ''))
        # self.preamble.append(Command('fancypagestyle', 'firstpage', NoEscape(r'\fancyhead[L]{\includegraphics[height=2cm]{io_helpers/assets/logo_left.png}} \fancyhead[R]{\includegraphics[height=2cm]{io_helpers/assets/logo_right.png}}')))
        # with self.create(Section('', numbering=False)) as header:
        #     with self.create(Tabular('lr')) as table:
        #         table.add_row(NoEscape(r'\includegraphics[width=2cm]{io_helpers/assets/logo_left.png}'),
        #                       NoEscape(r'\includegraphics[width=2cm]{io_helpers/assets/logo_right.png}'))
        # self.append(Command('thispagestyle', 'firstpage'))

        self.append(NoEscape(r'\maketitle'))

        self.append(NoEscape(r'\begin{multicols}{2}'))

        with self.create(Section('Device Information', numbering=False)):
            with self.create(Tabular('ll')) as table:
                table.add_row((bold('Device:'), self.config.metadata['device']))
                table.add_row((bold('Manufacturer:'), self.config.metadata['manufacturer']))
                table.add_row((bold('Serial Number:'), self.config.metadata['serial_number']))
                table.add_row((bold('Firmware Version:'), self.config.metadata['FW_version']))

        with self.create(Section('Operator Information', numbering=False)):
            with self.create(Tabular('ll')) as table:
                table.add_row((bold('Operator:'), self.config.metadata['operator']))
                table.add_row((bold('Date of Scans:'), self.config.metadata['datetime']))

        self.append(NoEscape(r'\end{multicols}'))
        self.append(NoEscape(r'\begin{multicols}{2}'))

        with self.create(Section('Environmental Conditions', numbering=False)):
            with self.create(Tabular('ll')) as table:
                table.add_row((bold('Temperature:'), str(self.config.metadata['temp'])))
                table.add_row((bold('Humidity:'), str(self.config.metadata['humidity'])))
                table.add_row((bold('Pressure:'), str(self.config.metadata['pressure'])))

        with self.create(Section('Comment', numbering=False)):
            with self.create(Tabular('l')) as table:
                table.add_row((self.config.metadata['comment'],))

        self.append(NoEscape(r'\end{multicols}'))
        self.append(NoEscape(r'\vspace{0.5cm}'))

        if self.config.ftp:
            with self.create(Section('Test Performance', numbering=False)):
                with self.create(Tabular('ll')) as table:
                    table.add_row((bold(NoEscape(r'$u_{TLS\_ISO}$:')), str(round(self.test.u_ISO_TLS*1e3, 3)) + 'mm'))
                    if self.config.case == 'a':
                        table.add_row((bold(NoEscape(r'$u_{ms}$:')), str(round(self.test.u_ms*1e3, 3)) + 'mm'))
                    if self.config.case == 'b':
                        table.add_row((bold(NoEscape(r'$u_{p}$:')), str(round(self.test.u_p*1e3, 3)) + 'mm'))
        elif self.config.stp:
            with self.create(Section('TLS uncertainty', numbering=False)):
                with self.create(Tabular('ll')) as table:
                    table.add_row((bold(NoEscape(r'$u_{T}$:')), str(round(self.test.u_t*1e3, 3)) + 'mm'))

        with self.create(Section('Results', numbering=False)):
            with self.create(Tabular('lll')) as table:
                table.add_row(f'max deviation:', f'{str(round(self.test.max_dev*1e3, 3)).rjust(6)}mm', '')
                table.add_hline()
                for key, value in self.test.results.items():
                    if abs(value) <= self.test.max_dev:
                        check = NoEscape(r'\begin{tikzpicture}\fill[green] (0,0) rectangle (0.3,0.3);\end{tikzpicture}')
                    else:
                        check = NoEscape(r'\begin{tikzpicture}\fill[red] (0,0) rectangle (0.3,0.3);\end{tikzpicture}')
                    table.add_row(f'{key}:', f'{str(round(value*1e3, 3)).rjust(6)}mm', check)

def generate_report(test, config):
    """
    Generate a PDF report for ISO 17123-9 test results.

    Args:
    - test (object): Instance of the test results (either Simplified or Full).
    - config (object): Configuration object containing metadata and test parameters.
    """
    report = PDF_report(test, config)
    if config.pdf[-4:] == '.pdf':
        p = config.pdf[:-4]
    else:
        p = config.pdf
    report.generate_pdf(p)
