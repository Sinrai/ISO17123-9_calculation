from pylatex import Document, Tabularx, Section, Command
from pylatex.utils import NoEscape, bold
import pylatex.config as cf

class PDF_report(Document):
    def __init__(self, test, config):
        geometry_options = {'tmargin': '1.5cm', 'lmargin': '1.5cm', 'rmargin': '1.5cm', 'bmargin': '1.5cm'}
        super().__init__('article', geometry_options=geometry_options, document_options=['a4paper'])

        self.test = test
        self.config = config

        self.preamble.append(Command('title', Command('textbf', f'ISO 17123-9 test report')))

        self.preamble.append(Command('date', config.current_dt))
        self.preamble.append(Command('pagenumbering', 'gobble'))
        self.append(NoEscape(r'\maketitle'))

        self.append('Lorem Ipsum')

def generate_report(test, config):
    report = PDF_report(test, config)
    if config.pdf[-4:] == '.pdf':
        p = config.pdf[:-4]
    else:
        p = config.pdf
    report.generate_pdf(p)
