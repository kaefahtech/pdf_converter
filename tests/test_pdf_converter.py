import sys
import pdftotext
import pytest
from io import StringIO
from pathlib import Path
from typing import TextIO
from configparser import ConfigParser



sys.path.append('/home/kojampef/Apps/vic/vara/book_converters/pdf_converter')
from pdf_converter.pdf_converter import PdfConverterFactory


@pytest.fixture
def config():
    config = ConfigParser()
    config.read('/home/kojampef/configs/pdf_converter.ini')
    return config


@pytest.fixture
def pdf_conv_factory():
    pdf_title = 'Site Reliability Engineering.pdf'
    return PdfConverterFactory(pdf_title)


@pytest.fixture
def pdf():
    with open('/home/kojampef/Books/pdfs/Site Reliability Engineering.pdf', 'rb') as pdf_file:
        pdf = pdftotext.PDF(pdf_file)
    return pdf

# TODO Test config file
#@pytest.mark.skip
def test_can_read_config_file(config):
    config['BOOKS'] = {'BASEDIR': '/home/kojampef/Books'}
    config['BOOKS']['PDFDIR'] = f"{config['BOOKS']['basedir']}/pdfs"
    config['BOOKS']['TEXTDIR'] = f"{config['BOOKS']['basedir']}/texts"

    configfile: TextIO
    home_dir = Path.home()
    config_path = home_dir / 'configs' / 'pdf_converter.ini'
    with open(config_path, 'w') as configfile:
        config.write(configfile)


# TODO Test PdfFactory class attributes
def test_pdffactory_class(config, pdf_conv_factory, pdf):
    assert isinstance(pdf_conv_factory, PdfConverterFactory)
    assert isinstance(pdf_conv_factory.config, ConfigParser)
    assert config.sections() == ['BOOKS']
    assert pdf_conv_factory.books_dir == '/home/kojampef/Books'
    assert pdf_conv_factory.pdf_dir == '/home/kojampef/Books/pdfs'
    assert pdf_conv_factory.text_dir == '/home/kojampef/Books/texts'
    assert pdf_conv_factory.pdf_title == Path('/home/kojampef/Books/pdfs/'
                                          'Site Reliability Engineering.pdf')
    assert pdf_conv_factory.text_title == Path('/home/kojampef/Books/texts/'
                                           'Site Reliability Engineering.txt')
    assert type(pdf_conv_factory.pdf) == type(pdf)
    assert pdf_conv_factory.page_count == len(pdf)

# TODO Test PdfFactory methods
def test_has_read_pdf_method(pdf_conv_factory, pdf):
    # TODO Can call read_pdf method and return a pdftotext object
    result = pdf_conv_factory.read_pdf()
    assert type(result) == type(pdf)


def test_can_throw_exception_if_pdf_file_does_not_exist():
    # TODO read_pdf can thrown exception if pdf file does not exist
    pdf_title = 'Fake Pdf Book.pdf'
    with pytest.raises(Exception) as exp:
        PdfConverterFactory(pdf_title)
    assert str(exp.value) == 'Fake Pdf Book.pdf does not exist in /home/kojampef/Books/pdfs'


def test_can_read_pages_on_screen(pdf_conv_factory, pdf, monkeypatch):
    # TODO Create page iterator
    monkeypatch.setattr('builtins.input', lambda: 'n')
    print(pdf_conv_factory.page_count)
    pdf_conv_factory.read_book()

def test_can_write_pdf_to_text_file(pdf_conv_factory, pdf):
    pdf_conv_factory.write_book()
    assert Path('/home/kojampef/Books/texts/Site Reliability Engineering.txt').exists()
    # TODO Write pdf to text file

