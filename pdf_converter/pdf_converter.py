import pdftotext
import sys
from pathlib import Path
from configparser import ConfigParser as cp
from os import system


class PdfConverterFactory:
    """ Test class to test imports"""

    def __init__(self, *args):
        self.config = cp()
        home_dir = Path.home()
        config_file = home_dir / 'configs' / 'pdf_converter.ini'
        self.config.read(config_file)
        self.books_dir = self.config.get('BOOKS', 'basedir')
        self.pdf_dir = self.config.get('BOOKS', 'pdfdir')
        self.text_dir = self.config.get('BOOKS', 'textdir')

        # Setting up pdf title
        pdf_title = self.config['BOOKS']['pdfdir'] + f"/{args[0]}"
        self.pdf_title = Path(pdf_title)

        # Setting up text title
        text_title = self.config['BOOKS']['textdir'] + f"/{args[0].split('.')[0]}.txt"
        self.text_title = Path(text_title)

        # Read the file
        try:
            self.__pdf = self.read_pdf()
        except Exception:
            raise Exception(f"{args[0]} does not exist in {self.pdf_dir}")
            

        # Count the pages
        self.page_count = len(self.pdf)

    @property
    def pdf(self):
        return self.__pdf


    @pdf.setter
    def pdf(self, pdf):
        self.__pdf = pdf


    def read_pdf(self):
        """ Converts pdf to text"""
        with open(self.pdf_title, 'rb') as pdf_file:
            self.pdf = pdftotext.PDF(pdf_file)
        return self.pdf

    def print_page(self, page):
        system('clear')
        system('clear')
        print('\n\n\n\n\n\n\n\n\n')
        print(self.pdf[page])

    def read_book(self):
        page = -1
        print("\nWelcome to BookReader1.0\n\n".center(200))

        user_choice = None
        while user_choice != 'x':
            print("\n\n\n[n] Enter n to go to next page")
            print('[p] Enter p to go to previous page')
            print('[f] Enter f to go to front cover')
            print('[b] Enter b to go to back cover')
            print('Enter a number to read a particular page')
            print('[x] Enter x to quit')
            print("Enter a value from the menu: ")
            user_choice = input()

            if user_choice == 'n':
                try:
                    page = page + 1
                    if page >= self.page_count:
                        self.print_page(-1)
                        print('\n\n\nYou are at the last page')
                    else:
                        self.print_page(page)
                except IndexError:
                    print('There are no more pages to read in this book')
            elif user_choice == 'p':
                page = page - 1
                if page <= 0:
                    self.print_page(0)
                    print('You are looking at the front cover page now')
                else:
                    self.print_page(page)
            elif user_choice == 'f':
                page = 0
                self.print_page(page)
            elif user_choice == 'b':
                page = -1
                self.print_page(page)
            elif user_choice == 'x':
                print('Closing book...')
            else:
                try:
                    page = int(user_choice)
                    self.print_page(page)
                except ValueError:
                    system('clear')
                    print('\n\n\n\nPlease enter a valid input')
                except IndexError:
                    system('clear')
                    print(f'\n\n\n\nPage not found, this book only has {self.page_count} pages.')
                    
    def write_book(self):
        with open(self.text_title, 'w') as text_file:
            text = "\n\n".join(self.pdf)
            text_file.write(text)


if __name__=="__main__":
    pdf_factory = PdfConverterFactory(sys.argv[1])
    if sys.argv[2] == 'r':
        pdf_factory.read_book()
    elif sys.argv[2] == 'w':
        pdf_factory.write_book()
    elif sys.argv[2] == 'rw':
        pdf_factory.write_book()
        pdf_factory.read_book()
    else:
        raise ValueError("Please enter a valid input")
