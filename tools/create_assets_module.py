import argparse
import glob
import os.path
import os
import base64


parser = argparse.ArgumentParser()

def create_folder(module_name):
    try:
        os.mkdir(module_name)
    except FileExistsError:
        pass
    

def get_bitmap_filepaths(folderpath, mask_suffix):
    folderpath = os.path.split(folderpath)
    all_files = glob.glob(os.path.join(*folderpath, "*.xbm"))
    return [fp for fp in all_files if not fp.endswith(f"{mask_suffix}.xbm")]


def get_photo_filepaths(folderpath):
    exts = ["gif", "ppm", "pgm"]
    rv = []
    folderpath = os.path.split(folderpath)
    for ext in exts:
        rv.extend(glob.glob(os.path.join(*folderpath, f"*.{ext}")))
    return rv


def get_bitmap_file_contents(path, mask_suffix):
    *filepath, filename = os.path.split(path)
    mask_filename = filename.split(".")[0] + f'{mask_suffix}.' + filename.split(".")[1]
    varname = filename.split(".")[0].replace("-", "_")
    code = ""
    code += varname + " = "
    with open(os.path.join(*filepath, filename)) as f:
        code += '"""\n' + "".join([line for line in f]) + '"""\n'
    code += f"\n{varname}_mask = "
    with open(os.path.join(*filepath, mask_filename)) as f:
        code += '"""\n' + "".join([line for line in f]) + '"""\n'
    return varname, code


def get_photo_file_contents(path):
    *filepath, filename = os.path.split(path)
    varname = filename.split(".")[0].replace("-", "_")
    code = varname + " = "
    with open(os.path.join(*filepath, filename), "rb") as f:
        code += '"""' + base64.b64encode(f.read()).decode("utf8") + '"""'
    return varname, code


def write_bitmap_code():
    for filepath in get_bitmap_filepaths(args.folderpath, args.masksuffix):
        py_fname, pycode = get_bitmap_file_contents(filepath, args.masksuffix)
        with open(os.path.join("dist", args.modulename, py_fname + ".py"), "w") as f:
            f.write(pycode)
        with open(os.path.join("dist", args.modulename, "__init__.py"), "a") as f:
            f.write(f"from .{py_fname} import {py_fname}, {py_fname + '_mask'}\n")


def write_photo_code():
    for filepath in get_photo_filepaths(args.folderpath):
        print(filepath)
        py_fname, pycode = get_photo_file_contents(filepath)
        with open(os.path.join("dist", args.modulename, py_fname + ".py"), "w") as f:
            f.write(pycode)
        with open(os.path.join("dist", args.modulename, "__init__.py"), "a") as f:
            f.write(f"from .{py_fname} import {py_fname}\n")


parser.add_argument("-folderpath", default="assets")
parser.add_argument("-modulename", default=None)
parser.add_argument("-masksuffix", default="-mask")
parser.add_argument("filetype", type=str, choices=("bitmap", "photo"))
args = parser.parse_args()
if args.modulename is None:
    args.modulename = args.filetype + "_assets"

create_folder("dist")
create_folder(os.path.join("dist", args.modulename))

if args.filetype == "bitmap":
    write_bitmap_code()

if args.filetype == "photo":
    write_photo_code()
