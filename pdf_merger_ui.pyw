import os
import json
from collections import namedtuple
from optparse import OptionParser
from typing import Tuple
import PySimpleGUI as sg
import pdf_merger as pm


def load_args() -> Tuple:
    parser = OptionParser(version=pm.VERSION)
    parser.add_option("-l", "--lang", dest="lang", help="Language", metavar="[lang]",
                      default="en")

    return parser.parse_args()


if __name__ == "__main__":
    lang = {}
    options, args = load_args()

    if not os.path.isfile(f"./lang/{options.lang}.json"):
        options.lang = "en"

    with open(f"./lang/{options.lang}.json", encoding="utf8") as f:
        lang = json.loads(f.read())

    sg.theme("SystemDefaultForReal")

    layout = [
        [sg.Text(lang["inputFiles"])],
        [sg.Input(), sg.FilesBrowse(button_text=lang["browse"],
                                    file_types=((lang["PDFFiles"], "*.pdf"), (lang["ALLFiles"], "*.*")))],
        [sg.Checkbox(lang["importBookmarks"], default=True),
         sg.Checkbox(lang["fileNameBookmarks"], default=True)],
        [sg.Text(lang["outputFile"])],
        [sg.Input(), sg.FileSaveAs(button_text=lang["saveAs"],
                                   file_types=((lang["PDFFiles"], "*.pdf"), (lang["ALLFiles"], "*.*")),
                                   default_extension="pdf")],
        [sg.OK(lang["create"]), sg.Quit(lang["quit"])]
    ]

    window = sg.Window(lang["name"], layout, icon="./icon.ico")

    while True:
        val = window.read()
        if val is None:
            continue

        event, values = val
        if event == sg.WIN_CLOSED or event == lang["quit"]:
            break
        if event == lang["create"] and values[lang["saveAs"]] != "" and values[lang["browse"]] != "":
            tmp_args_dict = {
                "output_file_name": values[lang["saveAs"]],
                "file_name_bookmarks": values[2],
                "import_bookmarks": values[1],
                "quiet": True
            }

            pm.create((namedtuple("ObjectName", tmp_args_dict.keys())(*tmp_args_dict.values()),
                       sorted(values[lang["browse"]].split(';'))))

    window.close()
