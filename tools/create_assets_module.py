import argparse
import glob
import os.path
import os
import base64


def create_folder(folder):
    """ Creates a folder """
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass
    

def get_bitmap_filepaths(folderpath, mask_suffix="-mask"):
    """ 
    Gets bitmap filepaths from a folder, doesn't return the masks.
    
    :param folderpath: the path to look into for bitmap files
    :param mask_suffix: ("-mask") the suffix appended to masks for X11 bitmap files
    :returns: list of filepaths
    """
    folderpath = os.path.split(folderpath)
    all_files = glob.glob(os.path.join(*folderpath, "*.xbm"))
    return [fp for fp in all_files if not fp.endswith(f"{mask_suffix}.xbm")]


def get_photo_filepaths(folderpath):
    """ 
    Gets photo filepaths from a folder, only returns *.gif, *.ppm, *.pgm files.
    
    :param folderpath: the path to look into for photo files
    :returns: list of filepaths
    """
    exts = ["gif", "ppm", "pgm"]
    rv = []
    folderpath = os.path.split(folderpath)
    for ext in exts:
        rv.extend(glob.glob(os.path.join(*folderpath, f"*.{ext}")))
    return rv


def get_bitmap_file_contents(path, mask_suffix="-mask"):
    """
    Gets the file contents of a bitmap file
    
    :param path: path to the file
    :type path: str
    :param mask_suffix: ("-mask") suffix for the mask file
    :type mask_suffix: str
    :returns: tuple (varname, code) of the variable name for that bitmap, and the resulting python code to write
    :rtype: tuple(str, str)
    """
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
    """
    Gets the file contents of a photo file
    
    :param path: path to the file
    :type path: str
    :returns: tuple (varname, code) of the variable name for that photo image, and the resulting python code to write
    :rtype: tuple(str, str)
    """
    *filepath, filename = os.path.split(path)
    varname = filename.split(".")[0].replace("-", "_")
    code = varname + " = "
    with open(os.path.join(*filepath, filename), "rb") as f:
        code += '"""' + base64.b64encode(f.read()).decode("utf8") + '"""'
    return varname, code


def write_bitmap_code():
    """
    Writes the bitmap code to the proper file, and add the relevant import to __init__.py
    """
    for filepath in get_bitmap_filepaths(args.folderpath, args.masksuffix):
        py_fname, pycode = get_bitmap_file_contents(filepath, args.masksuffix)
        with open(os.path.join("dist", args.modulename, py_fname + ".py"), "w") as f:
            f.write(pycode)
        with open(os.path.join("dist", args.modulename, "__init__.py"), "a") as f:
            f.write(f"from .{py_fname} import {py_fname}, {py_fname + '_mask'}\n")


def write_photo_code():
    """
    Writes the photo code to the proper file, and add the relevant import to __init__.py
    """
    for filepath in get_photo_filepaths(args.folderpath):
        print(filepath)
        py_fname, pycode = get_photo_file_contents(filepath)
        with open(os.path.join("dist", args.modulename, py_fname + ".py"), "w") as f:
            f.write(pycode)
        with open(os.path.join("dist", args.modulename, "__init__.py"), "a") as f:
            f.write(f"from .{py_fname} import {py_fname}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--folderpath", "-fp", default="assets",
                        help="Path to the folder to look into for assets, defaults to './assets'")
    parser.add_argument("--modulename", "-M", default=None,
                        help="Name of the resulting python module. If not specified, defaults to "
                             "('bitmap_assets', 'photo_assets'), depending on which asset type you run this program for")
    parser.add_argument("--masksuffix", "--mask", "-m", default="-mask", help="mask suffix for bitmap files.")
    parser.add_argument("filetype", type=str, choices=("bitmap", "photo"),
                        help="File type of the assets you want to run this program for.")
    args = parser.parse_args()
    if args.modulename is None:
        args.modulename = args.filetype + "_assets"

    create_folder("dist")
    create_folder(os.path.join("dist", args.modulename))

    if args.filetype == "bitmap":
        write_bitmap_code()

    if args.filetype == "photo":
        write_photo_code()
