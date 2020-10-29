# -*- coding: utf-8 -*-
import sys
from os import path
from optparse import OptionParser
from typing import Tuple
from datetime import datetime
from PyPDF2 import utils, PdfFileReader, PdfFileMerger


def load_args(version) -> Tuple:
    parser = OptionParser(version=version)

    parser.add_option("-o", "--output", dest="output_file_name", help="Output filename", metavar="[file name]",
                      default=f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")

    parser.add_option("-d", "--disable_file_name_bookmarks", dest="file_name_bookmarks", action="store_false", default=True,
                      help="File names will not be added to bookmarks")

    parser.add_option("-D", "--no_bookmark_import", dest="import_bookmarks", action="store_false", default=True,
                      help="Doesn't import bookmarks from source pdfs. Has no effect on the file name bookmarks.")

    options, args = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        exit(1)

    return (options, args)


def main():
    options, args = load_args("1.0.0")

    valid_pdfs = []

    for file in args:
        try:
            pdf = PdfFileReader(open(file, "rb"))
        except(IOError):
            print(f"\u001b[31;1m{file} could not be found. This file will be skipped!\u001b[0m")
        except(utils.PdfReadError):
            print(f"\u001b[33;1m{file} is not a valid pdf. This file will be skipped!\u001b[0m")
        else:
            valid_pdfs.append((pdf, path.basename(file)))

    pdf_merger = PdfFileMerger()
    for pdf_obj, pdf_name in valid_pdfs:
        if options.file_name_bookmarks:
            pdf_merger.append(pdf_obj, pdf_name, import_bookmarks=options.import_bookmarks)
        else:
            pdf_merger.append(pdf_obj, import_bookmarks=options.import_bookmarks)

    pdf_merger.write(options.output_file_name)
    print(f"'{options.output_file_name}' file has been successfully created!")


if __name__ == "__main__":
    main()
