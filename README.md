# Python PDF Merger

## Usage

Simply run the `pdf_merger.py` file.

```
usage: pdf_merger.py [-h] -f [file name] [[file name] ...] [-o [file name]] [-d] [-D] [-q]

PDF Merger v2.0.0

options:
  -h, --help            show this help message and exit
  -f [file name] [[file name] ...], --file [file name] [[file name] ...]
                        PDF files to merge
  -o [file name], --output [file name]
                        Output filename
  -d, --disable-file-name-bookmarks
                        File names will not be added to bookmarks
  -D, --no-bookmark-import
                        Doesn't import bookmarks from source PDFs
  -q, --quiet           No text will be written to stdout
```

### 3rd party package(s): `PyPDF2`

---

## License

This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.
