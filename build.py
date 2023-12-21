from argparse import ArgumentParser
import platform
import sys
import os
import shutil
import subprocess as sb

FILE_DIR = os.path.dirname(sys.argv[0])
LANG_DIR = os.path.join(FILE_DIR, "lang")
BIN_DIR = os.path.join(FILE_DIR, "build", "bin")

FILES = {
    "icon": os.path.join(FILE_DIR, "icon.ico"),
    "license": os.path.join(FILE_DIR, "LICENSE"),
    "readme": os.path.join(FILE_DIR, "README.md")
}

CMD_ARGS = {
    "cli": os.path.join(FILE_DIR, "pdf_merger.py"),
    "ui": os.path.join(FILE_DIR, "pdf_merger_ui.pyw"),
    "cli_name": "PDF Merger",
    "ui_name": "PDF Merger UI"
}


def get_cmd(is_win: bool, is_ui: bool) -> str:
    file = CMD_ARGS['cli']
    name = CMD_ARGS['cli_name']
    if is_ui:
        file = CMD_ARGS['ui']
        name = CMD_ARGS['ui_name']

    extra_args = ""
    if is_win:
        extra_args = f"--win-private-assemblies -i {FILES['icon']}"

    # pyinstaller==5.13.2 needed
    return f"pyinstaller \"{file}\" -n \"{name}\" --onefile {extra_args} --workpath=\"./build/tmp\" --distpath=\"./build/bin\""


def pkg(is_win: bool, is_ui: bool):
    pkg_dir = os.path.join(FILE_DIR, "build", "pkg")
    if not os.path.exists(pkg_dir):
        os.mkdir(pkg_dir)

    pkg_name = "pdf_merger_cli"
    if is_ui:
        pkg_name = "pdf_merger_ui"

    arc_type = "gztar"
    if is_win:
        arc_type = "zip"

    shutil.make_archive(os.path.join(pkg_dir, pkg_name), arc_type, BIN_DIR)
    return


def build(is_ui: bool):
    bin_lang_dir = os.path.join(BIN_DIR, "lang")

    shutil.copytree(LANG_DIR, bin_lang_dir, dirs_exist_ok=True)
    shutil.copyfile(FILES["icon"],
                    os.path.join(BIN_DIR, "icon.ico"))
    shutil.copyfile(FILES["license"],
                    os.path.join(BIN_DIR, "LICENSE"))
    shutil.copyfile(FILES["readme"],
                    os.path.join(BIN_DIR, "README.md"))

    sb.call(get_cmd(platform.system() == "Windows", is_ui))
    return


def clean():
    if os.path.isdir(os.path.join(FILE_DIR, "build", "tmp")):
        shutil.rmtree(os.path.join(FILE_DIR, "build", "tmp"))
    if os.path.isdir(os.path.join(FILE_DIR, "__pycache__")):
        shutil.rmtree(os.path.join(FILE_DIR, "__pycache__"))

    if os.path.isfile(os.path.join(FILE_DIR, f"{CMD_ARGS['cli_name']}.spec")):
        os.remove(os.path.join(FILE_DIR, f"{CMD_ARGS['cli_name']}.spec"))
    if os.path.isfile(os.path.join(FILE_DIR, f"{CMD_ARGS['ui_name']}.spec")):
        os.remove(os.path.join(FILE_DIR, f"{CMD_ARGS['ui_name']}.spec"))


print("Starting...")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", dest="pkg", action="store_true", default=False)
    parser.add_argument("-b", dest="build", action="store_true", default=False)
    parser.add_argument("-c", dest="clean", action="store_true", default=False)

    parser.add_argument("--cli", dest="cli", action="store_true", default=False)
    parser.add_argument("--ui", dest="ui", action="store_true", default=False)

    args = parser.parse_args()

    if args.build:
        build(args.ui)

    EXE_BIN = CMD_ARGS['cli_name']
    if args.ui:
        EXE_BIN = CMD_ARGS['ui_name']

    if platform.system() == "Windows":
        EXE_BIN = EXE_BIN + ".exe"

    exe_bin_path = os.path.join(BIN_DIR, EXE_BIN)
    if args.pkg and os.path.exists(exe_bin_path):
        pkg(platform.system() == "Windows", args.ui)

    if args.clean:
        clean()

    print("DONE!")
