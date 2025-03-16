import shutil
import os
import sys

from static_site_gen.file_handler import (
    copy_files_recursive,
    generate_pages_recursive,
)


def main():
    print(sys.argv)
    if len(sys.argv) == 1:
        basepath = "/"
    elif len(sys.argv) != 1:
        basepath = sys.argv[1]
    if os.path.exists("./docs"):
        shutil.rmtree("./docs")
    copy_files_recursive("./static", "./docs")
    generate_pages_recursive("./content/", "./template.html", "./docs/", basepath)


if __name__ == "__main__":
    main()
