import shutil
import os

from static_site_gen.file_handler import (
    copy_files_recursive,
    generate_pages_recursive,
)


def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    copy_files_recursive("./static", "./public")
    generate_pages_recursive("./content/", "./template.html", "./public/")


if __name__ == "__main__":
    main()
