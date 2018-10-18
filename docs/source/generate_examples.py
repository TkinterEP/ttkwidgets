# Examples documentation builder
import os

HEADER = "Example: {}"
TEMPLATE = \
    "{}\n" \
    "{}\n" \
    "\n" \
    ".. code-block:: python\n" \
    "\n" \
    "   {}"

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(FILE_DIR, "..", "..", "examples")
EXAMPLES = os.listdir(FOLDER)

EXAMPLES_FILE = \
    "Examples\n" \
    "========\n" \
    ".. toctree::\n" \
    "   :maxdepth: 2\n\n" \
    "   {}"

if not os.path.exists("examples"):
    os.makedirs("examples")

example_files = list()

for example in EXAMPLES:
    path = os.path.join(FOLDER, example)
    with open(path) as fi:
        lines = fi.readlines()
    text = "   ".join(lines)
    package, widget = None, None
    for line in lines:
        if "from ttkwidgets" in line:
            elems = line.replace("from", "").split("import")
            package, widget = map(str.strip, elems)
            break
    if widget is None:
        print("[WARNING] Could not determine imported widget in {}".format(example))
        continue
    package = package.split(".")
    package = "" if len(package) != 2 else package[1]

    header = HEADER.format(widget)
    text = TEMPLATE.format(header, "=" * len(header), text)

    out_path = os.path.join("examples", package)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    out_file = os.path.join(out_path, widget + ".rst")

    with open(out_file, "w") as fo:
        fo.write(text)

    example_files.append(out_file.replace(".rst", "") + "\n")

with open("examples.rst", "w") as fo:
    fo.write(EXAMPLES_FILE.format("   ".join(sorted(example_files))))


