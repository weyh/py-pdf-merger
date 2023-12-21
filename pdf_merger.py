import os
import re
from optparse import OptionParser
from typing import List, Tuple
from datetime import datetime
from PyPDF2 import errors, PdfReader, PdfMerger

VERSION = "1.1.0"


def load_args() -> Tuple:
    parser = OptionParser(version=VERSION)

    parser.add_option("-o", "--output", dest="output_file_name", help="Output filename",
            metavar="[file name]",
            default=f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")

    parser.add_option("-d", "--disable_file_name_bookmarks", dest="file_name_bookmarks",
            action="store_false", default=True,
            help="File names will not be added to bookmarks")

    parser.add_option("-D", "--no_bookmark_import", dest="import_bookmarks",
            action="store_false", default=True,
            help="Doesn't import bookmarks from source pdfs. Has no effect on the file name bookmarks.")

    parser.add_option("-q", "--quiet", dest="quiet", action="store_true", default=False,
            help="No text will be written to stdout.")

    options, args = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        exit(1)

    return (options, args)


def get_selection(file_list: list) -> List[str]:
    selected_files:  List[str] = []

    regex_a = re.compile(r"(\/|\\|^)\*.pdf$")
    regex_b = re.compile(r"(\/|\\|^)\*(.\*|)$")

    for file in file_list:
        if regex_a.search(file):  # *.pdf
            folder = os.path.dirname(file)

            if not folder:
                folder = "./"

            for f in os.listdir(folder):
                if len(f) >= 4 and f[-4:] == ".pdf":
                    selected_files.append(os.path.join(folder, f))
        elif regex_b.search(file):  # *, *.*
            folder = os.path.dirname(file)

            if not folder:
                folder = "./"

            for f in os.listdir(folder):
                selected_files.append(os.path.join(folder, f))
        else:
            selected_files.append(file)

    return selected_files


def print_q(text: str, quiet: bool):
    if not quiet:
        print(text)


def create(_args: Tuple):
    options, args = _args

    valid_pdfs: List[Tuple[str, str]] = []

    for file in get_selection(args):
        with open(file, "rb") as s:
            try:
                _ = PdfReader(s)
                valid_pdfs.append((file, os.path.basename(file).replace(".pdf", "")))
            except errors.PdfReadError:
                print_q(f"\u001b[33;1m{file} is not a valid pdf. This file will be skipped!\u001b[0m", options.quiet)
            except IOError:
                print_q(f"\u001b[31;1m{file} thrown an IOError. This file will be skipped!\u001b[0m", options.quiet)

    pdf_merger = PdfMerger()
    for pdf_file, pdf_name in valid_pdfs:
        if options.file_name_bookmarks:
            pdf_merger.append(pdf_file, pdf_name, import_outline=options.import_bookmarks)
        else:
            pdf_merger.append(pdf_file, import_outline=options.import_bookmarks)

    pdf_merger.write(options.output_file_name)
    print_q(f"'{options.output_file_name}' file has been successfully created!", options.quiet)


if __name__ == "__main__":
    create(load_args())
