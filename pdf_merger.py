from dataclasses import dataclass
import os
import re
from argparse import ArgumentParser
from typing import List, Tuple
from datetime import datetime
from PyPDF2 import errors, PdfReader, PdfMerger

VERSION = "2.0.0"

@dataclass
class Args:
    files: List[str]
    output_file_name: str
    file_name_bookmarks: bool
    import_bookmarks: bool
    quiet: bool

def load_args() -> Args:
    parser = ArgumentParser(description=f"PDF Merger v{VERSION}")

    parser.add_argument("-f", "--file",
            dest="files",
            nargs='+',
            required=True,
            default=f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf",
            metavar="[file name]",
            help="PDF files to merge")

    parser.add_argument("-o", "--output",
            dest="output_file_name",
            default=f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf",
            metavar="[file name]",
            help="Output filename")

    parser.add_argument("-d", "--disable-file-name-bookmarks",
            dest="file_name_bookmarks",
            action="store_false",
            default=True,
            help="File names will not be added to bookmarks")

    parser.add_argument("-D", "--no-bookmark-import",
            dest="import_bookmarks",
            action="store_false",
            default=True,
            help="Doesn't import bookmarks from source PDFs")

    parser.add_argument("-q", "--quiet",
            dest="quiet",
            action="store_true",
            default=False,
            help="No text will be written to stdout")

    args = parser.parse_args()

    if len(vars(args)) == 0:
        parser.print_help()
        exit(1)

    return Args(**vars(args))


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


def create(args: Args):
    valid_pdfs: List[Tuple[str, str]] = []

    for file in get_selection(args.files):
        with open(file, "rb") as s:
            try:
                _ = PdfReader(s)
                valid_pdfs.append((file, os.path.basename(file).replace(".pdf", "")))
            except errors.PdfReadError:
                print_q(f"\u001b[33;1m{file} is not a valid pdf. This file will be skipped!\u001b[0m", args.quiet)
            except IOError:
                print_q(f"\u001b[31;1m{file} thrown an IOError. This file will be skipped!\u001b[0m", args.quiet)

    pdf_merger = PdfMerger()
    try:
        for pdf_file, pdf_name in valid_pdfs:
            if args.file_name_bookmarks:
                pdf_merger.append(pdf_file, pdf_name, import_outline=args.import_bookmarks)
            else:
                pdf_merger.append(pdf_file, import_outline=args.import_bookmarks)

        pdf_merger.write(args.output_file_name)
    finally:
        pdf_merger.close()

    print_q(f"'{args.output_file_name}' file has been successfully created!", args.quiet)


if __name__ == "__main__":
    create(load_args())
