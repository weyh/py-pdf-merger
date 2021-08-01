from optparse import OptionParser
import platform
import sys
import os
import shutil
import subprocess as sb

file_dir = os.path.dirname(sys.argv[0])
lang_dir = os.path.join(file_dir, "lang")
bin_dir = os.path.join(file_dir, "build", "bin")

files = {
    "icon": os.path.join(file_dir, "icon.ico"),
    "license": os.path.join(file_dir, "LICENSE"),
    "readme": os.path.join(file_dir, "README.md")
}

cmd_args = {
    "cli": os.path.join(file_dir, "pdf_merger.py"),
    "ui": os.path.join(file_dir, "pdf_merger_ui.pyw"),
    "cli_name": "PDF Merger",
    "ui_name": "PDF Merger UI"
}


def get_cmd(is_win: bool, is_ui: bool) -> str:
    file = cmd_args['cli']
    name = cmd_args['cli_name']
    if is_ui:
        file = cmd_args['ui']
        name = cmd_args['ui_name']

    extra_args = ""
    if is_win:
        extra_args = f"--win-private-assemblies -i {files['icon']}"

    return f"pyinstaller \"{file}\" -n \"{name}\" --onefile {extra_args} --workpath=\"./build/tmp\" --distpath=\"./build/bin\""


def pkg(is_win: bool, is_ui: bool):
    pkg_dir = os.path.join(file_dir, "build", "pkg")
    if not os.path.exists(pkg_dir):
        os.mkdir(pkg_dir)

    pkg_name = "pdf_merger_cli"
    if is_ui:
        pkg_name = "pdf_merger_ui"

    arc_type = "gztar"
    if is_win:
        arc_type = "zip"

    shutil.make_archive(os.path.join(pkg_dir, pkg_name), arc_type, bin_dir)
    return


def build(is_ui: bool):
    bin_lang_dir = os.path.join(bin_dir, "lang")

    shutil.copytree(lang_dir, bin_lang_dir, dirs_exist_ok=True)
    shutil.copyfile(files["icon"],
                    os.path.join(bin_dir, "icon.ico"))
    shutil.copyfile(files["license"],
                    os.path.join(bin_dir, "LICENSE"))
    shutil.copyfile(files["readme"],
                    os.path.join(bin_dir, "README.md"))

    sb.call(get_cmd(platform.system() == "Windows", is_ui))
    return


def clean():
    if os.path.isdir(os.path.join(file_dir, "build", "tmp")):
        shutil.rmtree(os.path.join(file_dir, "build", "tmp"))
    if os.path.isdir(os.path.join(file_dir, "__pycache__")):
        shutil.rmtree(os.path.join(file_dir, "__pycache__"))

    if os.path.isfile(os.path.join(file_dir, f"{cmd_args['cli_name']}.spec")):
        os.remove(os.path.join(file_dir, f"{cmd_args['cli_name']}.spec"))
    if os.path.isfile(os.path.join(file_dir, f"{cmd_args['ui_name']}.spec")):
        os.remove(os.path.join(file_dir, f"{cmd_args['ui_name']}.spec"))


print("Starting...")

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", dest="pkg", action="store_true", default=False)
    parser.add_option("-b", dest="build", action="store_true", default=False)
    parser.add_option("-c", dest="clean", action="store_true", default=False)

    parser.add_option("--cli", dest="cli", action="store_true", default=False)
    parser.add_option("--ui", dest="ui", action="store_true", default=False)

    options, args = parser.parse_args()

    if options.build:
        build(options.ui)

    exe_bin = cmd_args['cli_name']
    if options.ui:
        exe_bin = cmd_args['ui_name']

    if platform.system() == "Windows":
        exe_bin = exe_bin + ".exe"

    exe_bin_path = os.path.join(bin_dir, exe_bin)
    if options.pkg and os.path.exists(exe_bin_path):
        pkg(platform.system() == "Windows", options.ui)

    if options.clean:
        clean()

    print("DONE!")
