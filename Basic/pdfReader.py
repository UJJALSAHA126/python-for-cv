import PyPDF2


def main():
    x = PyPDF2.PdfFileReader('demoPdf.pdf')
    print(x.getPage(2).extractText())


if __name__ == '__main__':
    main()
    