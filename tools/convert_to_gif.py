import mimetypes
import argparse
import os
import os.path
import glob
from PIL import Image
from json import loads


def get_all_images(folder_path, except_exts=None):
    """
    Gets all images from a folder path, except the ones with extensions in `except_exts`
    
    :param except_exts: list or tuple of extentions for which images should not be matched and returned
    :type except_exts: NoneType or list or tuple
    :returns: list of filepaths
    :rtype: list
    """
    if except_exts is None:
        except_exts = ["gif", "ppm", "pgm"]
    path = os.path.join(*os.path.split(folder_path), "*.*")
    rv = []
    for fpath in glob.glob(path):
        ftype =  mimetypes.guess_type(fpath)[0].split("/")[0]
        ext = fpath.split(".")[-1]
        if ftype == "image" and ext not in except_exts:
            rv.append(fpath)
    return rv
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--folderpath", "-fp", default="assets",
                        help="path to load the images from")
    parser.add_argument("--outputpath", "-o", default="assets/gifs",
                        help="path to save the resulting images into")
    parser.add_argument("--except_exts", "-e", default=None, type=str, 
                        help="Do not convert these extensions, must be a json formatted list of strings.")
    parser.add_argument("--verbosity", "-v", default=False, type=bool,
                        help="toggle verbose output")
    args = parser.parse_args()

    if args.except_exts is not None:
        args.except_exts = loads(args.except_exts)

    os.makedirs(args.outputpath, exist_ok=True)

    for image_path in get_all_images(args.folderpath, args.except_exts):
        if args.verbosity:
            print(f"Processing {image_path}")
        img = Image.open(image_path)
        path = os.path.split(image_path)
        img_name = path[-1].split(".")[0]
        new_name = os.path.join(*os.path.split(args.outputpath), 
                                img_name + ".gif")
        img.save(new_name)
        if args.verbosity:
            print(f"Saved image as {new_name}")
    